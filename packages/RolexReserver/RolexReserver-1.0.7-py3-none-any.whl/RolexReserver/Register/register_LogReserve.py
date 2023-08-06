from LibHanger.Library.DataAccess.uwPostgres import uwPostgreSQL
from RolexReserver.Register.Base.baseRegister import baseRegister

class register_LogReserve(baseRegister):
    
    """
    データ一括登録クラス
    """
    
    def __init__(self, __psgr:uwPostgreSQL):
        
        """
        コンストラクタ
        """
        
        # 基底側コンストラクタ
        super().__init__(__psgr)
    