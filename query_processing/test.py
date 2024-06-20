from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, QuantoConfig
import torch
from model_config import model_name
from langchain_huggingface import HuggingFacePipeline



quantization_config = QuantoConfig(weights="float8")

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map = "auto", trust_remote_code=True, quantization_config=quantization_config)

prompt = """System: You are an expert in Question and Answering tasks specifically regarding rare diseases, focusing on Hypophosphatasia and Ehlers-Danlos Syndrome. 
    You will be given relevant context to answer user queries. 
    Answer the user query only using the given context and ensure your response is accurate, clear, and concise. 
    Do not mention in your response that you were given context. Do not reference the context in your response at all.

    "Years of investigations showed that Ehlers-Danlos syndrome is a disorder with a very complex phenotype and highly complicated genotype. 
    Publisher\\'s Note: MDPI stays neutral with regard to jurisdictional claims in published maps and institutional affiliations.", 
    "Ehlers-Danlos syndrome (EDS) is a heterogeneous group of heritable connective tissue disorders. 
    The 2017 International Classification of EDS recognizes 13 subtypes caused by pathogenic variants in 19 different genes, 
    encoding different types of collagen or protein involved in collagen metabolism (Table 1). 
    The most abundant types of EDS are classical (cEDS), vascular (vEDS), and hypermobile (hEDS); all EDS types, except hEDS, have their genetic backgrounds determined. 
    According to the newest classification, classical EDS is inherited as an autosomal dominant disorder caused by mutations in COL5A1, COL5A2, or c.934C>T in COL1A1. 
    For the clinical diagnosis of cEDS, major and minor criteria were established. 
    cEDS should be suspected when skin hyperextensibility and atrophic scars are present (major criterion 1), 
    together with joint hypermobility assessed with the Beighton score (major criterion 2), 
    and/or with at least three minor criteria 
    (easy bruising, soft, doughy skin, skin fragility, molluscoid pseudotumors, subcutaneous spheroids, hernias (or history thereof), epicanthal folds, complications of 
    joint hypermobility (e.g., sprains, dislocations/subluxations, pain, pes planus), and family history of a first-degree relative who meets clinical criteria). 
    Clinical features included in EDS classification are only one part of the disabilities recognized in EDS patients. 
    In addition to major and minor phenotype criteria, patients\\' clinical picture also contains dysfunction of the gastrointestinal, cardiovascular, immune, neural, and other systems. 
    The clinical symptoms may differ among patients within the same family and may occur at different ages with various intensities. 
    It is worth noting that not all cEDS patients with a pathogenic variant in the COL5A1 or COL5A2 gene fulfil the criteria for classical type EDS diagnosis according to the International Classification (Table 1). 
    Some may share their symptoms with other types of EDS (mainly with hypermobile, classical-like, or vascular) or other connective tissue disorders, and establishing their diagnosis is possible only after molecular investigation. 
    Diagnosis of cEDS must be established based on clinical criteria and confirmed by molecular analysis. 
    Genetic testing was primarily based on single-gene testing by Sanger sequencing (COL5A1, COL5A2, and c.934C>T in COL1A1). 
    However, nowadays, because of phenotypic heterogeneity and clinical overlapping among EDS types and between EDS and other connective tissue disorders, 
    single-gene testing conducted after clinical evaluation is often not definitive and leaves EDS patients without a molecular diagnosis. Molecular testing with next-generation sequencing (NGS) and a multigene panel, containing EDS-related and other connective tissue-associated genes (for diagnosis specifying), seems to be a very adequate method. In the present study, we evaluated the molecular background of Polish cEDS patients by NGS with an Illumina connective tissue gene panel.", 'The Ehlers-Danlos syndromes (EDS) consist of 13 subtypes with overlapping features including joint hypermobility, skin, and vascular fragility and generalised connective tissue friability. Current major criteria for classical EDS (cEDS) are (1) skin hyperextensibility and atrophic scars and (2) joint hypermobility. Minor criteria are easy bruising, soft doughy skin, skin fragility, molluscoid pseudotumors, subcutaneous spheroids, hernia(s), epicanthal folds, complications of joint hypermobility, and an affected first degree relative. The minimal criteria for a diagnosis of cEDS are major criterion 1 plus either major criterion 2 or 3 of the 9 minor criteria. In patients who satisfy the main criteria of cEDS according to the Villefranche criteria, the variant detection rate in either COL5A1 or COL5A2 is over 90%. However, intrafamilial variability in classical EDS has been reported. There are 194 reported unique variants reported in the COL5A1 gene. These genes encode collagen type V, a fibrillar heterotrimer ([alpha1(V)]2 alpha2(V)) that is present in a wide variety of tissues but is particularly prevalent in bone, skin and tendon. Collagen type V accounts for approximately 5% of total body collagen and has a role in maintaining the deposition and structure of other more abundant collagens, particularly collagen type I. Rarely, a diagnosis of cEDS is due to dominant variants in COL1A1 or COL1A2. For many years, skin biopsies for electron microscopy (EM) have been recommended as a first line of investigation to confirm or exclude a diagnosis of cEDS. This was due to the occurrence of collagen flowers visible by EM. Collagen flowers in individuals with classical EDS were described by Vogel et al. who reported collagen fibrils with an abnormally large diameter and a highly irregular and lobulated contour interspersed with normal appearing fibrils with a mean diameter larger than that of collagen fibrils in normal skin. A longitudinal section showed that the large atypical fibrils were seen to be poorly integrated filamentous aggregates. Variation in frequency of very large highly irregular fibrils differed per patient but in general constituted approximately 5%. These very large highly-irregular fibrils are often described as longitudinally splayed and loosely packed fibrils, which in cross section produce the collagen flower pattern. Although it is known that collagen flowers can be found in other collagen disorders including osteogenesis imperfecta and Ullrich congenital muscular dystrophy, typical collagen flowers were thought to be invariably present in people with cEDS. Given the high detection rates of pathogenic variants in cEDS, current recommendations are that electron microscopy based on a skin biopsy should no longer the first line of investigation but could be used to clarify inconclusive molecular results, or to guide further testing if initial molecular testing is negative. Interestingly, it was mentioned that "the absence of typical collagen flowers would go against the diagnosis, as there are no known reports of patients with type V collagen abnormalities without collagen flowers on EM". Here, we report for the first time two patients, one fulfilling the clinical diagnosis of classical EDS and one not, with (likely) pathogenic variants in COL5A1 and absence of collagen flowers on EM.'

    By looking at the above context, answer the following user question.

    User: What other genes are associated or might be associated with TNXB variants that cause clEDS?

    Assistant:"""


tokenized_prompt = tokenizer(tokenizer.bos_token + prompt, return_tensors="pt").to(model.device)
terminators = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
]
outputs = model.generate(input_ids=tokenized_prompt.input_ids, attention_mask=tokenized_prompt.attention_mask, max_new_tokens=128, eos_token_id=terminators)



response = outputs[0][tokenized_prompt.input_ids.shape[-1]:]
print(tokenizer.decode(response, skip_special_tokens=True))

