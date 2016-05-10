#encoding=utf-8
import re
import base64
from itsdangerous import URLSafeTimedSerializer as USTS
#自定义文件加密密钥
file_security_key='qwhdgskfsdf'
#文件类型
file_ok_suffix=['pdf','ppt','doc','docx','xls','xlsx','txt','mobi','epub']

def create_name(user_name,filename):
	suffix = re.split('\W+',filename)[-1]
	insert_db=False
	if suffix in file_ok_suffix:
		key0 = file_security_key
		key1 = base64.encodestring(key0)
		new_name = USTS(key0).dumps(user_name,key1)+'.'+suffix
		insert_db=True
	else:
		new_name=''
	return insert_db,new_name