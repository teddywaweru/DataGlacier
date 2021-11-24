import spacy
from spacy.training import Example      #imported in scenarios where the NER model is to be fed preprocessed data
from spacy.tokens import Doc, Span
from spacy import displacy
# nlp = spacy.load("en_core_web_sm")
import random
import json

#Utilizing the Spacy resume format
def train_model_sp(train_ds):
    nlp = spacy.blank('en') #create a blank entity model
    if 'ner' not in nlp.pipe_names:     
        ner = nlp.add_pipe('ner')       #adding the ner component to the pipeline

    for _, annotation in train_ds:                  
        for entity in annotation['entities']:    #loop through the dataset to select the entity labels to be used by the component
            ner.add_label(entity[2])

                

    optimizer = nlp.begin_training()            #optimizer declaration
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):       #disable all other components in the pipeline
        for itn in range(2):                    #Number of iterations for training the model
            print('Starting iteration')
            # random.shuffle(train_ds)          #Randomize the data in the set?
            losses = {}
            index = 0
            # batches = spacy.util.minibatch(train_ds, size = 10)
            for batch in batches:
                print(batch)
                texts, annotations = zip(*batch)
            for text, annotation in train_ds:
                try:
                    nlp.update(
                        texts,
                        annotations,
                        drop = 0.2,
                        sgd = optimizer,
                        losses = losses
                        )

                    # nlp.update(
                    #     [example2],
                    #     drop = 0.2,
                    #     sgd = optimizer,
                    #     losses = losses
                    # )
                except Exception as e:
                    pass
                # print(spacy.training.offsets_to_biluo_tags(nlp.make_doc(item['content']), annotation))
                print(losses)
                # print(text)
                # print(annotation)


#Utilizing the DataTurk resume format
def train_model_dt(train_ds):
    nlp = spacy.blank('en') #create a blank entity model
    if 'ner' not in nlp.pipe_names:     
        ner = nlp.add_pipe('ner')       #adding the ner component to the pipeline

    for item in train_ds:                  
        for entities in item['annotation']:     
            for entity in entities['label']:    #loop through the dataset to select the entity labels to be used by the component
                ner.add_label(entity)
                

    optimizer = nlp.begin_training()            #optimizer declaration
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):       #disable all other components in the pipeline
        for itn in range(3):                    #Number of iterations for training the model
            print('Starting iteration')
            random.shuffle(train_ds)          #Randomize the data in the set?
            losses = {}
            index = 0
            for item in train_ds:
                doc = nlp(item['content'])      #Resume content converted to nlp doc against which the model is to train
                
                annotation = list(zip([x['start'] for x in (y['points'][0] for y in item['annotation'])],   #start values
                                        [x['end'] +1 for x in (y['points'][0] for y in item['annotation'])],  #end values
                                        [x['label'][0] if x['label'] != [] else 'NaN' for x in item['annotation']],  #labels filtering for blanks
                                        [x['text'] for x in (y['points'][0] for y in item['annotation'])]
                                        )) 
                
                #intended for updating the doc.ents with the labels from the dataset.
                #Has been commented due to the errors caused by the overlapping entities
                # doc_tokens = find_tokens(annotation, doc)
                # doc.set_ents([Span(doc, token[0], token[1], token[2]) for token in doc_tokens])

                annotation, annotation_dup = check_annotation(annotation)       #Verify on overlapping entities & return annotation list
                example1 = Example.from_dict(doc, {'entities' : annotation})
                example2 = Example.from_dict( doc, {'entities' : annotation_dup})

                #Print token entities & tokens
                # eg = example1.to_dict()
                # print([(x, y) for x, y in zip(eg['doc_annotation']['entities'],eg['token_annotation']['ORTH'])])

                try:
                    nlp.update(
                        [example1],
                        drop = 0.2,
                        sgd = optimizer,
                        losses = losses
                        )

                    nlp.update(
                        [example2],
                        drop = 0.2,
                        sgd = optimizer,
                        losses = losses
                    )
                except Exception as e:
                    pass

                # displacy.serve(doc,style = 'ent')
                print(losses)
    nlp.to_disk('nlp_model')


def spacy_load_model(model):
    nlp_model = spacy.load(model)
    return nlp_model

# Check integrity of the annotations in the list
def check_annotation(annotation):
    rmv_idx = []                        #list to hold annotations to be removed
    dup_tags = []
    dup_words = []
    annotation_dup = []
    
    annotation = list(set(annotation))  #remove duplicate entities
    # for i in rmv_idx:
    #     print(annotation[i])
    for item in annotation:
        for comp_item in annotation:    #iterative loops to compare values against each other
            if comp_item != item:       #skip similar tuples
                if (item[0] <= comp_item[0] <= item[1]) or (item[0] <= comp_item[1] <= item[1]):      #check if item has start value between start & end values of other item
                    # print('Comparative Item: \t{} \n Item: \t\t\t{}' .format(comp_item, item))
                    # if ((item[1] - item[0]) > (comp_item[1] - comp_item[0])):
                        # doc = nlp(item_['annotation']['points'][0]['text'])
                    if item[:3] in annotation_dup: #Disregard item that is already in the annotation_dup
                        pass
                    else:    
                        dup_tags = comp_item[2]
                        dup_words = comp_item[3]
                        annotation_dup.append(comp_item[:3])
                        rmv_idx.append(annotation.index(comp_item))
    for x in sorted(list(set(rmv_idx)),  reverse = True):               #iterate through the list of reverse ordered & unique values of rmv_idx  
        annotation.pop(x)                                               # pop
    return ([i[:3] for i in annotation], list(set(annotation_dup)))


def load_data(file_path):
    resume_dt = []
    with open(file_path, encoding = 'utf8') as data:
    # resume_dt = pd.read_json(data, lines = True) #Works for typical json files, however this file type comprises of json lines without separators
        for line in data:
            resume_dt.append(dict(json.loads(line)))        #Read each line on its own & load to memory. Number of lines can also be curated.
    
    from dataturks_spacy_conv import convert_dataturks_to_spacy 
    resume_sp = convert_dataturks_to_spacy(file_path)
    return(resume_sp, resume_dt)


def find_tokens(annotation, doc):
    doc_tokens = []
    for entity in annotation:
        if entity[3] in doc.text[entity[0] : entity[1]]:
            first_token = doc.char_span(entity[0], entity[1], alignment_mode = 'expand')[0].i
            last_token = doc.char_span(entity[0], entity[1], alignment_mode = 'expand')[-1].i
            doc_tokens.append((first_token, last_token + 1, entity[2]))

    return doc_tokens