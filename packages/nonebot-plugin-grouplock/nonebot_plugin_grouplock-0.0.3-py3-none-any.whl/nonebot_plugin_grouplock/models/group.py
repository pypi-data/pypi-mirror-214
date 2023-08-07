from tortoise import fields
from tortoise.models import Model


class GroupSetting(Model):
    id: int = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增主键，数据库ID"""
    time: int = fields.IntField()
    """创建时间戳"""
    group_id: int = fields.IntField()
    """群号"""
    group_name: int = fields.TextField()
    """群名称"""
    group_memo: str = fields.TextField(null=True)
    """群备注"""
    group_create_time: int = fields.IntField()
    """群创建时间"""
    group_level: int = fields.IntField()
    """群等级"""
    member_count: int = fields.IntField()
    """成员数"""
    max_member_count: int = fields.IntField()
    """最大成员数"""
    set_count: int = fields.IntField()
    """设置群最大人数"""
    check_status: bool = fields.BooleanField(default=False)
    """检查开关"""
    auto_kick: bool = fields.BooleanField(default=False)
    """启动锁定群人数"""

    class Meta:
        table = 'GroupSetting'
        table_description = '群设置'
        indexes = ('time', 'group_id',)


class GroupMember(Model):
    id: int = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增主键，数据库ID"""
    time: int = fields.IntField()
    """创建时间戳"""
    group_id: int = fields.IntField()
    """群号"""
    user_id: int = fields.IntField()
    """QQ号"""
    nickname: str = fields.TextField(null=True)
    """昵称"""
    card: str = fields.TextField(null=True)
    """群名片"""
    sex: str = fields.TextField(null=True)
    """性别"""
    age: int = fields.IntField(null=True)
    """年龄"""
    area: str = fields.TextField(null=True)
    """地区"""
    join_time: int = fields.IntField()
    """加群时间"""
    last_sent_time: int = fields.IntField(null=True)
    """最后发言时间"""
    level: str = fields.TextField(null=True)
    """成员等级"""
    role: str = fields.TextField(null=True)
    """角色"""
    unfriendly: bool = fields.BooleanField(default=False)
    """是否不良记录成员"""
    title: str = fields.TextField(null=True)
    """头衔"""
    title_expire_time: int = fields.IntField(null=True)
    """头衔过期时间"""
    card_changeable: bool = fields.BooleanField(default=True)
    """是否允许修改群名片"""
    shut_up_timestamp: int = fields.IntField(null=True)
    """禁言到期时间"""

    class Meta:
        table = 'GroupMember'
        table_description = '群成员'
        indexes = ('time', 'group_id',)
