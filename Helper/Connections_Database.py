# %% Admin
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import pyodbc
import time
import sqlite3

# %% Odin Connection
def connect_to_odinprod():

    # Cloud Connection Information
    default_credential = DefaultAzureCredential()
    secret_client = SecretClient(
        vault_url="https://keyvaultforquant.vault.azure.net/",
        credential=default_credential
    )
    temp_odin_server = "quantserver.database.windows.net,1433"
    temp_odin_username    = secret_client.get_secret(name="odinprodConnect-username")
    temp_odin_password    = secret_client.get_secret(name="odinprodConnect-password")

    # PYODBC String
    pyodbcodinprod_str = \
        'DRIVER=ODBC Driver 17 for SQL Server;' + \
        'SERVER=' + temp_odin_server + ';' +\
        'DATABASE=odin_prod;' +\
        'UID=' + temp_odin_username.value + ';' +\
        'PWD=' + temp_odin_password.value + ';' + \
        'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

    # PYODBC Object
    try:
        print("Determining status of the database: ")
        pyodbcodinprod_object = pyodbc.connect(pyodbcodinprod_str)
    except:
        print("~Database is sleeping, Starting the Database up!")
        time.sleep(60)
        pyodbcodinprod_object = pyodbc.connect(pyodbcodinprod_str)
    finally:
        print("~Odin Connection is ready!")

    return pyodbcodinprod_str, pyodbcodinprod_object
# conn_odin_str, conn_odin_obj= connect_to_odinprod()



# %% SQLite Connection
def connect_to_sqlite(Path_DB="D:\\DB_Odin\\Odin.db"):
    OdinConnect = sqlite3.connect(Path_DB)

    return(OdinConnect)
# conn_sqlite_object= connect_to_sqlite()
