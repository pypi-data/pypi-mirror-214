
from abc import ABC, abstractclassmethod
import jsonschema
import json

class ValidatorField(ABC):
    ''' Classe abstrata que serve como base para criar validadores 
    afim de retornar schemas do jsonschema versão do Draft-7'''

    @abstractclassmethod
    def to_schema(self) -> dict:
        ''' Retorna um dicionário que é a representação do schema'''
        pass
    
    @abstractclassmethod
    def to_error_msg(self) -> str:
        ''' Retorna uma mensagem de erro que foi atribuida ao validador.'''
        pass


class ValidatorRegex(ValidatorField):
    ''' Classe usada para criar jsonschema de validação de um regex'''
    __name = None
    __regex = None 
    __msg_error = ''
    
    def to_error_msg(self) -> str:
        return self.__msg_error

    def __str__(self) -> str:
        return self.__name

    def __init__(self, name: str, regex: str, msg_error: str = '') -> None:
        ''' Recebe o nome, a expressão regular (string) e opcionalmente uma mensagem de erro, 
        que caso inserida será chamada pelo validador.
        
        Parameters:
          name: Uma string que representa o nome do campo do schema a ser validado
          regex: Uma expressão regular para ser tratada na validação do campo
          msg_error: Mensagem de erro a ser acionada pelo validador caso o valor seja invalido.
          

        Examples:
          >>> v = ValidatorRegex('telefone', regex = '\([0-9]{2}\)9[0-9]{4}-[0-9]{4}', msg_error = 'Expressão não validada')

        '''
        self.__name = name
        self.__regex = regex
        self.__msg_error = msg_error
    
    def to_schema(self) -> dict:
        ''' Retorna o dicionario do schemajson
        
        Examples:
           >>> v = ValidatorRegex('telefone', regex = '\([0-9]{2}\)9[0-9]{4}-[0-9]{4}')
           >>> v.to_schema()
           >>> {"telefone": {"type": "string", "format": "regex", "pattern": "\([0-9]{2}\)9[0-9]{4}-[0-9]{4}"} }
        
        '''
        return {
            self.__name: {
            "type": "string", 
            "format": "regex", 
            "pattern": self.__regex
            } 
        }


class ValidatorString(ValidatorField):
    ''' Classe usada para criar o validador jsonschema para strings'''
    __name = None
    __min = None 
    __max = None
    __msg_error = None

    def to_error_msg(self) -> str:
        return self.__msg_error

    def __str__(self) -> str:
        return self.__name

    def __init__(self, name: str, min: int = None, max: int = None,  msg_error: str = '') -> None:
        ''' Recebe o nome e opcionalmente os valores min e max, além de uma mensagem de erro, 
        que caso inserida será chamada pelo validador.
        
        Parameters:
          name: Uma string que representa o nome do campo do schema a ser validado
          msg_error: Mensagem de erro a ser acionada pelo validador caso o valor seja invalido.
          min: Quantidade minima de caracteres aceitos
          max: Quantidade maxima de caracteres aceitos

        Examples:
          >>> v = ValidatorString('descricao', min = 1, max = 10, msg_error = 'Quantidade minima de 1 caractere e maxima de 10')

        '''
        self.__name = name
        self.__min = min 
        self.__max = max
        self.__msg_error = msg_error
    
    def to_schema(self) -> dict:
        ''' Retorna o dicionario do schemajson
        
        Examples:
           >>> v = ValidatorString('descricao', min = 3, max = 10)
           >>> v.to_schema()
           >>> { "descricao": {"type": "string", "minLength": 3, "maxLength": 10 } }
        '''
        validador = { self.__name: { "type": "string" } }

        if self.__min:
            validador[self.__name]['minLength'] = self.__min
        
        if self.__max:
            validador[self.__name]['maxLength'] = self.__max
        
        return validador


class ValidatorHour(ValidatorField):
    '''Classe usada para validar a hora enviada pelo usuário'''
    __name = None
    __msg_error = None

    def __init__(self, name: str, msg_error: str = '') -> None:
        '''Recebe o nome do campo e opcionalmente uma mensagem de erro 
        chamada pelo validador.
        
        Parameters:
          name: Uma string representa o nome do campo do schema ea ser validado
          msg_error: Mensagem de erro a ser acionada pelo validador em caso de erro.
        
        Examples:
          >>> v = ValidatorHour('hora', 'Formato não aceito')
        '''
        self.__name = name
        self.__msg_error = msg_error
    
    def to_schema(self) -> dict:
        ''' Retorna o dicionario do schemajson
        
        Examples:
            >>> v = ValidatorRegex('telefone', regex = '\([0-9]{2}\)9[0-9]{4}-[0-9]{4}')
            >>> v.to_schema()
            >>> {"telefone": {"type": "string", "format": "regex", "pattern": "\([0-9]{2}\)9[0-9]{4}-[0-9]{4}"} }
        
        '''
        return {
            self.__name: {
            "type": "string", 
            "format": "regex", 
            "pattern": '^([01]\d|2[0-3]):([0-5]\d)$'
            } 
        }

    def to_error_msg(self) -> str:
        return self.__msg_error

    def __str__(self) -> str:
        return self.__name


class ValidatorDate(ValidatorField):
    ''' Classe usada para criar o validador jsonschema para datas'''
    __name = None
    __msg_error = None

    def to_error_msg(self) -> str:
        return self.__msg_error

    def __str__(self) -> str:
        return self.__name

    def __init__(self, name: str, msg_error: str = '') -> None:
        ''' Recebe o nome e opcionalmente uma mensagem de erro 
        chamada pelo validador.
        
        Parameters:
          name: Uma string que representa o nome do campo do schema a ser validado
          msg_error: Mensagem de erro a ser acionada pelo validador caso o valor seja invalido.

        Examples:
          >>> v = ValidatorDate('data', 'Idade não permitida')

        '''
        self.__name = name
        self.__msg_error = msg_error
    
    def to_schema(self) -> dict:
        ''' Retorna o dicionario do schemajson
        
        Examples:
           >>> v = ValidatorDate('data')
           >>> v.to_schema()
           >>> { "data": { "type": "string", "format": "date" } }
        '''
        return { self.__name: { "type": "string", "format": "date" } }


class ValidatorNumber(ValidatorField):
    ''' Classe usada para criar o validador jsonschema para numeros'''
    __name = None
    __min = None 
    __max = None
    __msg_error = None

    def to_error_msg(self) -> str:
        return self.__msg_error

    def __str__(self) -> str:
        return self.__name

    def __init__(self, name: str, min: int = None, max: int = None, msg_error: str = '') -> None:
        ''' Recebe o nome e opcionalmente os valores min e max, além de uma mensagem de erro, 
        que caso inserida será chamada pelo validador.
        
        Parameters:
          name: Uma string que representa o nome do campo do schema a ser validado
          msg_error: Mensagem de erro a ser acionada pelo validador caso o valor seja invalido.
          min: Valor minimo aceito
          max: Valor maximo aceito

        Examples:
          >>> v = ValidatorNumber('idade', min = 18, max = 99, msg_error = 'Idade não permitida')

        '''
        self.__name = name
        self.__min = min 
        self.__max = max
        self.__msg_error = msg_error
    
    def to_schema(self) -> dict:
        ''' Retorna o dicionario do schemajson
        
        Examples:
           >>> v = ValidatorNumber('idade', min = 18, max = 99)
           >>> v.to_schema()
           >>> { "idade": {"type": "string", "minimum": 18, "maximum": 99 } }
        '''
        validador = { self.__name: { "type": "number" } }

        if self.__min:
            validador[self.__name]['minimum'] = self.__min
        
        if self.__max:
            validador[self.__name]['maximum'] = self.__max
        
        return validador


class ValidatorEnum(ValidatorField):
    ''' Classe usada para criar o validador jsonschema para enumeradores'''
    __name = None
    __enum = None
    __msg_error = None

    def to_error_msg(self) -> str:
        return self.__msg_error

    def __str__(self) -> str:
        return self.__name

    def __init__(self, name: str, enum: list, msg_error: str = '') -> None:
        ''' Recebe o nome e o enumerador, e opcionalmente uma mensagem de erro 
        chamada pelo validador.
        
        Parameters:
          name: Uma string que representa o nome do campo do schema a ser validado
          msg_error: Mensagem de erro a ser acionada pelo validador caso o valor seja invalido.
          enum: lista de valores a serem comparados para validação

        Examples:
          >>> v = ValidatorEnum('status', ['A', 'B', 'C'], 'Valor nao aceito')

        '''
        self.__name = name
        self.__enum = enum
        self.__msg_error = msg_error
    
    def to_schema(self) -> dict:
        ''' Retorna o dicionario do schemajson.
        
        Examples:
           >>> v = ValidatorEnum('status', ['A', 'B', 'C'])
           >>> v.to_schema()
           >>> { "status": {"type": "string", "enum":  ['A', 'B', 'C'] } }
        '''
        tipo = "number" if  isinstance(self.__enum[0], int) else "string"

        validador = { self.__name: { "type": tipo, "enum": self.__enum } }

        return validador


class Validator:
    ''' Usado para validar campos e criar schemas json.'''
    __validate_fields = None
    __schema = None


    @staticmethod
    def validate_json(form: any) -> dict:
        '''Recebe um objeto do tipo request e verifica se o campo 'dados' foi 
        enviado, e se o mesmo é um JSON.
        
        Parameters:
            form: Um parametro request dentro do contexto do Flask
        
        Examples:
            >>> Validator.validate_json(request) # O request do form contendo um body com 'dados' e um JSON.
            {'de': '2023', 'ate': '2023', 'grupos': '1', 'lojas': '1'}

            Caso o form não atenda ao padrão um retorno dict com atributo erro é recebido
            >>> Validator.validate_json(request) # 
            {"erro": "ESPERADO UM ATRIBUTO DADOS QUE NAO EXISTE", "codigo": 1}
        
        '''
        if not "dados" in form.form.keys():
            return {"erro": "CAMPO DADOS AUSENTE", "codigo": 1}
        # Veja se é json
        try:
            dados = json.loads(form.form["dados"])
        except json.decoder.JSONDecodeError:
            return {"erro": "FALHA, DADOS ENVIADOS NÃO SÃO UM JSON", "codigo": 2}

        return dados


    def __init__(self, list_validate_fields: list[ValidatorField], requireds: list[str]):
        ''' Recebe uma lista de parametros e os campos requeridos como obrigatórios 
        para montar o objeto schemajson.
        
        Parameters:
          list_validate_fields: Uma lista com ValidatorFields que sabem como retornar uma representação de campo do schema
          requireds: Lista de campos informados como requeridos
        
        Examples:
          >>> v = Validator([ ValidatorString('descricao', min = 3) ], ['descricao'])
        '''
        if len(list_validate_fields) == 0:
            raise ValueError('Necessário enviar ao menos um ValidatorField')
        
        self.__validate_fields = list_validate_fields
        self.__schema = {
            "type": "object", "properties": {}, "required": requireds,
        }

        for validate_field in list_validate_fields:
            if not isinstance(validate_field, ValidatorField):
                raise ValueError('Um dos campos enviados não é um ValidatorField')
            self.__schema['properties'].update(validate_field.to_schema())


    def is_valid(self, data: dict, format_checker:any = None) -> None:
        ''' Verifica se o schema enviado é valido, caso necessário é possível incluir um format_checker 
        que pode ser usado para validar campos, por exemplo do tipo date.
        Caso algum campo não seja validado um **ValueError** é lançado pelo método.

        Parameters:
          data: Um dicionario que representa os dados a serem validados
          format_checker: Um validador para algum tipo de campo especifico, por exemplo campos date
        
        Examples:
            >>> v = Validator([ ValidatorString('descricao', min = 3) ], ['descricao'])
            >>> v.is_valid({'descricao': 'Ola mundo'})

            >>> v2 = Validator([ ValidatorDate('data') ], ['data'], jsonschema.FormatChecker(["date"]))
            >>> v2.is_valid({'data': '2023-01-01'})
        '''

        v = jsonschema.Draft7Validator( self.__schema, format_checker = format_checker )
        # Veja se os dados são validos
        if not v.is_valid(data):
            # Pega os erros
            erros = v.iter_errors(data)
            for err in erros:
                
                try:
                    campo = list(err.absolute_path)[0]
                except IndexError:
                    campo = None
                #
                if campo is None:
                    raise ValueError('Objeto não condiz com o esperado')
                # Veja qual campo que deu erro
                if not campo is None:
                    print(campo)
                    validator_error = [ v for v in self.__validate_fields if str(v) == campo ][0]
                    raise ValueError(validator_error.to_error_msg())

