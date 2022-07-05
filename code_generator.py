from random import randint

class CodeGenerator:
    def __init__(self):
        self.statement_list = list()
        self.START_PHRASE = 'Stars are saying... '

        self.nouns_list = ['appearence', 'look', 'luck', 'friendship', 
                           'relationships', 'skills', 'body']
        self.NOUNS_NUMBER = len(self.nouns_list)
        self.used_nouns_indexes = list()

        self.adj_list = ['adorable', 'adventurous', 'amused', 'beautiful', 
                         'better', 'charming', 'cheerful', 'excellent',
                         'fine', 'funny', 'good', 'gorgeous', 
                         'kind', 'lovely', 'successful', 'tasty']
        self.ADJ_NUMBER = len(self.adj_list)
        self.used_adj_indexes = list()

    def get_next_noun(self):
        noun_ind = randint(0, self.NOUNS_NUMBER - 1)
        while noun_ind in self.used_nouns_indexes:
            noun_ind = randint(0, self.NOUNS_NUMBER - 1)

        self.used_nouns_indexes.append(noun_ind)
        
        noun = self.nouns_list[noun_ind]
        return noun

    def gen_next_adj(self):
        adj_ind = randint(0, self.ADJ_NUMBER - 1)
        while adj_ind in self.used_nouns_indexes:
            adj_ind = randint(0, self.NOUNS_NUMBER - 1)

        self.used_adj_indexes.append(adj_ind)

        adj = self.adj_list[adj_ind]
        return adj

    def add_statement(self):
        noun = self.get_next_noun()
        adj = self.gen_next_adj()
        self.statement_list.append(f'your {noun} will be {adj}')

    def gen_code(self):
        for i in range(5):
            self.add_statement()
        
        source_code = ''.join((self.START_PHRASE, ', '.join(self.statement_list), '.'))

        return source_code

def main():
    code_generator = CodeGenerator()
    code = code_generator.gen_code()
    print(code)

if __name__ == '__main__':
    main()