## Model Building: Training spaCy

In order to train the model using spaCy, we had to convert the Persian dataset into JSON format from CoNLL-U format. We do this using the following python command:
```
>> python -m spaCy convert [input_file] [output_dir]

>> python -m spacy convert fa_seraji-ud-train.conllu "C:\DATA"

>> python -m spacy convert fa_seraji-ud-dev.conllu "C:\DATA"
```
After that, we used the json formatted training data and the following command to build the models:
```
>> python -m spacy train [lang] [output_dir] [train_data] [dev_data] [epochs] [notagger] [no-ner]

>> python -m spacy train fa "C:\ALL_MODELS" fa_seraji-ud-train.json fa_seraji-uddev.json -n 20 -g 1 -T -N
```
We used 20 epochs and for each epoch the spaCy parser outputted a model. Note that, we also used the development data in order to evaluate the model’s performance while building it. So, out of 20 model we chose top 5 models based on the development data. We then evaluated those top 5 model using the test dataset to get the best model. The following command was used to evaluate the test data on those models:
```
>> python -m spacy evaluate model7 fa_seraji-ud-test.json -dp "C:\Parsed_Output"
```
The -dp command outputs 20 random dependency trees from the test data. Note that, we only evaluated the models in order to find the best model in this step. This result for the best model has also been mentioned in the result section.


## Model Building: Training UDPipe

For training the model for the UDPipe parser, we used the following command that it is easy to train a model for any language:
```
>> Python: udpipe --parse persian-ud-2.0-170801.udpipe fa_seraji-ud-test.conllu --outfile=out.conllu

>> Python: udpipe --accuracy --parse persian-ud-2.0-170801.udpipe fa_seraji-udtest.conllu --outfile=model_performance.txt
```
UDPipe has binary executable file for model training and evaluation. And we can directly get the conllu formatted parser output from the test data.
