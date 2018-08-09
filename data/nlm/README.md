Data extracted from [NLM RxNorm and Drug Interaction API](https://rxnav.nlm.nih.gov/APIsOverview.html).

`This product uses publicly available data from the U.S. National Library of Medicine (NLM), National Institutes of Health, Department of Health and Human Services; NLM is not responsible for the product and does not endorse or recommend this or any other product.`

---

Additional data extracted from [DrugCentral](http://drugcentral.org) published under [CC BY-SA](http://drugcentral.org/privacy).

Ursu, O., Holmes, J., Knockel, J., Bologa, C. G., Yang, J. J., Mathias, S. L., … Oprea, T. I. (2016). DrugCentral: online drug compendium. Nucleic Acids Research, 45(D1), D932–D939. https://doi.org/10.1093/nar/gkw993

Queries for data extraction:

    SELECT DISTINCT a.identifier as drugbank_id, b.identifier as rxnorm_id
      FROM identifier AS a
        JOIN identifier AS b ON a.struct_id=b.struct_id AND b.id_type = "RXNORM"
        WHERE a.id_type = "DRUGBANK_ID" ORDER BY a.identifier;
