import re
import pullenti_wrapper
from pullenti_wrapper.processor import Processor, ADDRESS, PERSON

class Anonymizer:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Anonymizer, cls).__new__(cls)
            cls.preprocessor = cls._init_preprocessor(cls)
        return cls.instance
    
    def anonymize(self, text):
        text = self._get_name_addr(text)
        text = self._get_mail(text)
        text = self._get_phone(text)
        text = self._get_numbers(text)        
        text = re.sub(r" +", " ", text)
        text = text.strip()
        return text
    
    def _get_mail(self, text):
        return re.sub(r'[\w\.-]+@[\w\.-]+', ' ', text)

    def _get_phone(self, text):
        return re.sub('\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}', ' ', text)
    
    def _get_numbers(self, text):
        return re.sub(r'\b\d{5}\b', ' ', text)

    def _get_name_addr(self, text):
        result = self.preprocessor(text)
        for m in result.matches:
            start = m.span.start
            stop = m.span.stop
            find = text[start:stop]
            replase = ' ' * (stop - start)
            text = text.replace(find, replase)
        return text

    def _init_preprocessor(self):
        return Processor([ADDRESS, PERSON])