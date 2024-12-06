#### Stemmer: Morphological Analyzer & Disambiguator

- This is an implementation of "The Role of Context in Neural Morphological Disambiguation", which can be found here: https://aclanthology.org/C16-1018.pdf
- There are slight modifications to the original paper:
	- My network uses GRU instead of LSTM, which decreases the number of parameters by 25% with no actual performance penalty.
	- My network has an extra Dense layer before output(p) layer.
	- My network optionally uses Concatenation instead of Addition while merging representations of stems & tags, and left & right surface form contexts.
	- My network optionally uses Deep RNNs, although current configuration results in single layer RNNs.
	- I shuffle the positions of candidates and labels in every batch.

- It is tested on below test sets:
	- trmorph2006: 0.9467 accuracy on ambigious tokens and 0.9664 accuracy on all tokens, compared to 0.910 and 0.964 in the original paper.
	- trmorph2018: 0.9376 accuracy on ambigious tokens and 0.9535 accuracy on all tokens
- Starting with 0.001 learning rate, lr decay of 0.95 is used after the 5th epoch.
- After development phase, final model in the repository is trained on all of train, test and handtagged sets of trmorph2006, trmorph2016 and trmorph2018 sets for 30 epochs. Therefore, in order to evaluate the model, initialize with StemmerAnalyzer(evaluate = True) to use the weights that were NOT trained using the test sets.
- As analyzer, it uses Yildiz's analyzer, which can be found here: https://github.com/erayyildiz/LookupAnalyzerDisambiguator