
pip install --upgrade --user awscli
path %PATH%;%USERPROFILE%\AppData\Roaming\Python\Scripts
aws --version

pip install boto

mkdir %USERPROFILE%\.aws
@echo off
(echo [default]
echo aws_access_key_id = AAAAAAAAAAAAAAAAAAAAAAAAAA
echo aws_secret_access_key = AAAAAAAAAAAAAAAAAAAAAAAAAAAA
)>>%USERPROFILE%\.aws\credentials.boto
echo on

@echo off
(echo [default]
echo region=us-east-1
)>>%USERPROFILE%\.aws\config.boto
echo on

