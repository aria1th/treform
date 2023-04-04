import json

from pycrfsuite_spacing import PyCRFSuiteSpacing
from pycrfsuite_spacing import TemplateGenerator
from pycrfsuite_spacing import CharacterFeatureTransformer


class BaseSegmentation:
    IN_TYPE = [str]
    OUT_TYPE = [str]


class SegmentationKorean(BaseSegmentation):
    def __init__(self, model=None):
        # model_path = 'demo_model.crfsuite'
        to_feature = CharacterFeatureTransformer(
            TemplateGenerator(
                begin=-2,
                end=2,
                min_range_length=3,
                max_range_length=3)
        )
        self.inst = PyCRFSuiteSpacing(to_feature)
        self.inst.load_tagger(model)

    def __call__(self, *args, **kwargs):
        return self.inst(args[0])



class LSTMSegmentationKorean(BaseSegmentation):
    def __init__(self, model_path='./model'):
        self.model = model_path
        dic_path = self.model + '/' + 'dic.pickle'

        # config
        self.n_steps = 30  # time steps
        self.padd = '\t'  # special padding chracter

    def __call__(self, *args, **kwargs):

        sentence = args[0]
        sentence_size = len(sentence)
        tag_vector = [-1] * (sentence_size + self.n_steps)  # buffer n_steps
        pos = 0

        return None

    def close(self):
        self.sess.close()


class CNNSegmentationKorean(BaseSegmentation):
    def __init__(self, model_file='./model', training_config='', char_file=''):
        self.model_file = model_file
        self.training_config = training_config
        self.char_file = char_file

        #self.model, self.vocab_table = self.load(model_file=model_file, training_config=training_config, char_file=char_file)


    def load(self, model_file='', training_config='', char_file=''):
        with open(training_config, encoding='utf-8') as f:
            config = json.load(f)

        return model, vocab_table

    def predict(self, model, vocab_table, input_str):
        inference = self.get_inference_fn(model, vocab_table)
        result = ''
        return b"".join(result).decode("utf8")

    def get_inference_fn(self, model, vocab_table):
        inference = None
        return inference


    #def __call__(self, *args, **kwargs):
    #    return self.predict(self.model, self.vocab_table, args[0])

def convert_output_to_string(byte_array, model_output):
    strings_result = None
    return strings_result

if __name__ == "__main__":
    model_file = '../../models/checkpoint-12.ckpt'
    training_config = '../../resources/config.json'
    char_file = '../../resources/chars-4996'

    spacing = CNNSegmentationKorean()

    model, vocab_table = spacing.load(model_file=model_file, training_config=training_config, char_file=char_file)
    input_str = '오늘은우울한날이야...ㅜㅜ'
    result = spacing.predict(model, vocab_table, input_str)
    result = result.replace('<s>','')
    result = result.replace('</s>', '')
    print(result)