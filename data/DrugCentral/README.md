# DrugCentral

Data extracted from [DrugCentral](http://drugcentral.org) published under [CC BY-SA](http://drugcentral.org/privacy).

Ursu, O., Holmes, J., Knockel, J., Bologa, C. G., Yang, J. J., Mathias, S. L., … Oprea, T. I. (2016). DrugCentral: online drug compendium. Nucleic Acids Research, 45(D1), D932–D939. https://doi.org/10.1093/nar/gkw993

Queries for drug interactions:

    SELECT DISTINCT d.identifier as id1, e.identifier as id2, a.ddi_risk
      FROM ddi as a
        JOIN drug_class as b ON a.drug_class1=b.name
        JOIN struct2drgclass as b2 ON b.id=b2.drug_class_id
        JOIN identifier as d ON b2.struct_id=d.struct_id AND d.id_type="DRUGBANK_ID"
        JOIN drug_class as c ON a.drug_class2=c.name
        JOIN struct2drgclass as c2 ON c.id=c2.drug_class_id
        JOIN identifier as e ON c2.struct_id=e.struct_id AND e.id_type="DRUGBANK_ID";
