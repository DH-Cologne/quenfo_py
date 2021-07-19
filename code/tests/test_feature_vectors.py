"""
TODO: Replikation der featurevector Generierung:

1. wir gehen von allen cus aus zusammen! dh aus dem alten loop raus! dann Für jede cu und die dazugehörigen fus wird überprüft, ob diese in fuo sind
    else: es wird eine fuo erstellt: Dafür werden alle fus einer cu geadded (und dabei werden duplikate rausgeworfen und alphabetische sortierung)#
    Alle fus werden der liste fuo hinzugefügt. dh nach diesem schritt gibt es nach wie vor die classifyunits mit ihren fus, aber es gibt auch noch
    eine Liste uniqueFeatureunits, die alle fus aller cus enthält (alphabetisch und sortiert)

2. initalisiere set FeatureValues (s. funktion unten aus Loglikelihood script)
    - hier wird das bow2 (aus den trainingsdaten) als bowtemp gesetzt und das bow1 erstellt. 
    - bow1 bekommt alle Featureunits einer cu geadded (kein remove von doppelten (deshalb add all)) (featureunitorder kommt erst unter punkt 3 ins spiel)
    - aus bowtemp werden die bow1 features gelöscht

    --> dh. ich habe hier jetzt drei bows: bow2 (aus trainingsdaten), bow1 (aus allen featureunits einer cu), bowtemp (kopie des bow2 abzüglich der bow1)

3. hier kommt die uniquefeatureunits liste ins spiel (aufgerufen über this.featureUnitOrder) --> wird zum scoring benötigt

-------------------------

public void setFeatureValues(List<ClassifyUnit> classifyUnits, List<String> featureUnitOrder) {
			
		this.featureUnitOrder = featureUnitOrder;
		if(featureUnitOrder==null){
			this.featureUnitOrder = getFeatureUnitOrder(classifyUnits);
			this.initialize(classifyUnits);
		}

		for (ClassifyUnit classifyUnit : classifyUnits) {
			Multiset<String> bowTemp =  HashMultiset.create(bagOfWords2);
			Multiset<String> bagOfWords1 = HashMultiset.create();
			bagOfWords1.addAll(classifyUnit.getFeatureUnits());
			bowTemp.removeAll(bagOfWords1);	
			
			List<ScoredItem<String>> llh = LogLikelihood.compareFrequencies(
					bagOfWords1, bowTemp, bagOfWords1.size(), 0.0);
			double[] featureVector = new double[this.featureUnitOrder.size()];
			for (int i = 0; i < this.featureUnitOrder.size(); i++) {
				double value = 0.0;
				String featureUnit = this.featureUnitOrder.get(i);
				
				for (ScoredItem<String> item : llh) {
					if (item.getItem().equals(featureUnit)) {
						value = item.getScore();
					}
				}
				featureVector[i] = value;
			}
			classifyUnit.setFeatureVector(featureVector);
		}
		
	}

"""

# Erster Test: Funktion (gen_featureunitorder)
# Input: eine cu (mit fus)
# todo: adde fus to fuso list, aber keine duplikate und sortiere liste alphabetisch
# output: liste fuso (alle zusammen von allen featureunits aller cus) (duplikate raus und sortiert)

import unittest

class TestSum(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_sum_tuple(self):
        self.assertEqual(sum((1, 2, 2)), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()