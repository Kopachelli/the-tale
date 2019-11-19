# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bank.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='bank.proto',
  package='bank',
  syntax='proto3',
  serialized_pb=_b('\n\nbank.proto\x12\x04\x62\x61nk\"d\n\tOperation\x12\x12\n\naccount_id\x18\x01 \x01(\r\x12\x10\n\x08\x63urrency\x18\x02 \x01(\x05\x12\x0e\n\x06\x61mount\x18\x03 \x01(\x05\x12\x0c\n\x04type\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\"Z\n\rHistoryRecord\x12\x12\n\ncreated_at\x18\x01 \x01(\x01\x12\x10\n\x08\x63urrency\x18\x02 \x01(\x05\x12\x0e\n\x06\x61mount\x18\x03 \x01(\x05\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t\"h\n\x08\x42\x61lances\x12,\n\x07\x61mounts\x18\x01 \x03(\x0b\x32\x1b.bank.Balances.AmountsEntry\x1a.\n\x0c\x41mountsEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\"/\n\x17\x41\x63\x63ountsBalancesRequest\x12\x14\n\x0c\x61\x63\x63ounts_ids\x18\x01 \x03(\r\"\x9b\x01\n\x18\x41\x63\x63ountsBalancesResponse\x12>\n\x08\x62\x61lances\x18\x01 \x03(\x0b\x32,.bank.AccountsBalancesResponse.BalancesEntry\x1a?\n\rBalancesEntry\x12\x0b\n\x03key\x18\x01 \x01(\r\x12\x1d\n\x05value\x18\x02 \x01(\x0b\x32\x0e.bank.Balances:\x02\x38\x01\"+\n\x15\x41\x63\x63ountHistoryRequest\x12\x12\n\naccount_id\x18\x01 \x01(\r\">\n\x16\x41\x63\x63ountHistoryResponse\x12$\n\x07history\x18\x01 \x03(\x0b\x32\x13.bank.HistoryRecord\"z\n\x17StartTransactionRequest\x12#\n\noperations\x18\x01 \x03(\x0b\x32\x0f.bank.Operation\x12\x10\n\x08lifetime\x18\x02 \x01(\x01\x12\x12\n\nautocommit\x18\x03 \x01(\x08\x12\x14\n\x0crestrictions\x18\x04 \x01(\t\"2\n\x18StartTransactionResponse\x12\x16\n\x0etransaction_id\x18\x01 \x01(\x04\"2\n\x18\x43ommitTransactionRequest\x12\x16\n\x0etransaction_id\x18\x01 \x01(\x04\"\x1b\n\x19\x43ommitTransactionResponse\"4\n\x1aRollbackTransactionRequest\x12\x16\n\x0etransaction_id\x18\x01 \x01(\x04\"\x1d\n\x1bRollbackTransactionResponse\"\x1a\n\x18\x44\x65\x62ugClearServiceRequest\"\x1b\n\x19\x44\x65\x62ugClearServiceResponseb\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_OPERATION = _descriptor.Descriptor(
  name='Operation',
  full_name='bank.Operation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_id', full_name='bank.Operation.account_id', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='currency', full_name='bank.Operation.currency', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='amount', full_name='bank.Operation.amount', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='type', full_name='bank.Operation.type', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='description', full_name='bank.Operation.description', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=20,
  serialized_end=120,
)


_HISTORYRECORD = _descriptor.Descriptor(
  name='HistoryRecord',
  full_name='bank.HistoryRecord',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='created_at', full_name='bank.HistoryRecord.created_at', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='currency', full_name='bank.HistoryRecord.currency', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='amount', full_name='bank.HistoryRecord.amount', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='description', full_name='bank.HistoryRecord.description', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=122,
  serialized_end=212,
)


_BALANCES_AMOUNTSENTRY = _descriptor.Descriptor(
  name='AmountsEntry',
  full_name='bank.Balances.AmountsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='bank.Balances.AmountsEntry.key', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='bank.Balances.AmountsEntry.value', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=_descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001')),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=272,
  serialized_end=318,
)

_BALANCES = _descriptor.Descriptor(
  name='Balances',
  full_name='bank.Balances',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='amounts', full_name='bank.Balances.amounts', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_BALANCES_AMOUNTSENTRY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=214,
  serialized_end=318,
)


_ACCOUNTSBALANCESREQUEST = _descriptor.Descriptor(
  name='AccountsBalancesRequest',
  full_name='bank.AccountsBalancesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='accounts_ids', full_name='bank.AccountsBalancesRequest.accounts_ids', index=0,
      number=1, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=320,
  serialized_end=367,
)


_ACCOUNTSBALANCESRESPONSE_BALANCESENTRY = _descriptor.Descriptor(
  name='BalancesEntry',
  full_name='bank.AccountsBalancesResponse.BalancesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='bank.AccountsBalancesResponse.BalancesEntry.key', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='bank.AccountsBalancesResponse.BalancesEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=_descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001')),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=462,
  serialized_end=525,
)

_ACCOUNTSBALANCESRESPONSE = _descriptor.Descriptor(
  name='AccountsBalancesResponse',
  full_name='bank.AccountsBalancesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='balances', full_name='bank.AccountsBalancesResponse.balances', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_ACCOUNTSBALANCESRESPONSE_BALANCESENTRY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=370,
  serialized_end=525,
)


_ACCOUNTHISTORYREQUEST = _descriptor.Descriptor(
  name='AccountHistoryRequest',
  full_name='bank.AccountHistoryRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_id', full_name='bank.AccountHistoryRequest.account_id', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=527,
  serialized_end=570,
)


_ACCOUNTHISTORYRESPONSE = _descriptor.Descriptor(
  name='AccountHistoryResponse',
  full_name='bank.AccountHistoryResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='history', full_name='bank.AccountHistoryResponse.history', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=572,
  serialized_end=634,
)


_STARTTRANSACTIONREQUEST = _descriptor.Descriptor(
  name='StartTransactionRequest',
  full_name='bank.StartTransactionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='operations', full_name='bank.StartTransactionRequest.operations', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='lifetime', full_name='bank.StartTransactionRequest.lifetime', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='autocommit', full_name='bank.StartTransactionRequest.autocommit', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='restrictions', full_name='bank.StartTransactionRequest.restrictions', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=636,
  serialized_end=758,
)


_STARTTRANSACTIONRESPONSE = _descriptor.Descriptor(
  name='StartTransactionResponse',
  full_name='bank.StartTransactionResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='transaction_id', full_name='bank.StartTransactionResponse.transaction_id', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=760,
  serialized_end=810,
)


_COMMITTRANSACTIONREQUEST = _descriptor.Descriptor(
  name='CommitTransactionRequest',
  full_name='bank.CommitTransactionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='transaction_id', full_name='bank.CommitTransactionRequest.transaction_id', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=812,
  serialized_end=862,
)


_COMMITTRANSACTIONRESPONSE = _descriptor.Descriptor(
  name='CommitTransactionResponse',
  full_name='bank.CommitTransactionResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=864,
  serialized_end=891,
)


_ROLLBACKTRANSACTIONREQUEST = _descriptor.Descriptor(
  name='RollbackTransactionRequest',
  full_name='bank.RollbackTransactionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='transaction_id', full_name='bank.RollbackTransactionRequest.transaction_id', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=893,
  serialized_end=945,
)


_ROLLBACKTRANSACTIONRESPONSE = _descriptor.Descriptor(
  name='RollbackTransactionResponse',
  full_name='bank.RollbackTransactionResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=947,
  serialized_end=976,
)


_DEBUGCLEARSERVICEREQUEST = _descriptor.Descriptor(
  name='DebugClearServiceRequest',
  full_name='bank.DebugClearServiceRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=978,
  serialized_end=1004,
)


_DEBUGCLEARSERVICERESPONSE = _descriptor.Descriptor(
  name='DebugClearServiceResponse',
  full_name='bank.DebugClearServiceResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1006,
  serialized_end=1033,
)

_BALANCES_AMOUNTSENTRY.containing_type = _BALANCES
_BALANCES.fields_by_name['amounts'].message_type = _BALANCES_AMOUNTSENTRY
_ACCOUNTSBALANCESRESPONSE_BALANCESENTRY.fields_by_name['value'].message_type = _BALANCES
_ACCOUNTSBALANCESRESPONSE_BALANCESENTRY.containing_type = _ACCOUNTSBALANCESRESPONSE
_ACCOUNTSBALANCESRESPONSE.fields_by_name['balances'].message_type = _ACCOUNTSBALANCESRESPONSE_BALANCESENTRY
_ACCOUNTHISTORYRESPONSE.fields_by_name['history'].message_type = _HISTORYRECORD
_STARTTRANSACTIONREQUEST.fields_by_name['operations'].message_type = _OPERATION
DESCRIPTOR.message_types_by_name['Operation'] = _OPERATION
DESCRIPTOR.message_types_by_name['HistoryRecord'] = _HISTORYRECORD
DESCRIPTOR.message_types_by_name['Balances'] = _BALANCES
DESCRIPTOR.message_types_by_name['AccountsBalancesRequest'] = _ACCOUNTSBALANCESREQUEST
DESCRIPTOR.message_types_by_name['AccountsBalancesResponse'] = _ACCOUNTSBALANCESRESPONSE
DESCRIPTOR.message_types_by_name['AccountHistoryRequest'] = _ACCOUNTHISTORYREQUEST
DESCRIPTOR.message_types_by_name['AccountHistoryResponse'] = _ACCOUNTHISTORYRESPONSE
DESCRIPTOR.message_types_by_name['StartTransactionRequest'] = _STARTTRANSACTIONREQUEST
DESCRIPTOR.message_types_by_name['StartTransactionResponse'] = _STARTTRANSACTIONRESPONSE
DESCRIPTOR.message_types_by_name['CommitTransactionRequest'] = _COMMITTRANSACTIONREQUEST
DESCRIPTOR.message_types_by_name['CommitTransactionResponse'] = _COMMITTRANSACTIONRESPONSE
DESCRIPTOR.message_types_by_name['RollbackTransactionRequest'] = _ROLLBACKTRANSACTIONREQUEST
DESCRIPTOR.message_types_by_name['RollbackTransactionResponse'] = _ROLLBACKTRANSACTIONRESPONSE
DESCRIPTOR.message_types_by_name['DebugClearServiceRequest'] = _DEBUGCLEARSERVICEREQUEST
DESCRIPTOR.message_types_by_name['DebugClearServiceResponse'] = _DEBUGCLEARSERVICERESPONSE

Operation = _reflection.GeneratedProtocolMessageType('Operation', (_message.Message,), dict(
  DESCRIPTOR = _OPERATION,
  __module__ = 'bank_pb2'
  # @@protoc_insertion_point(class_scope:bank.Operation)
  ))
_sym_db.RegisterMessage(Operation)

HistoryRecord = _reflection.GeneratedProtocolMessageType('HistoryRecord', (_message.Message,), dict(
  DESCRIPTOR = _HISTORYRECORD,
  __module__ = 'bank_pb2'
  # @@protoc_insertion_point(class_scope:bank.HistoryRecord)
  ))
_sym_db.RegisterMessage(HistoryRecord)

Balances = _reflection.GeneratedProtocolMessageType('Balances', (_message.Message,), dict(

  AmountsEntry = _reflection.GeneratedProtocolMessageType('AmountsEntry', (_message.Message,), dict(
    DESCRIPTOR = _BALANCES_AMOUNTSENTRY,
    __module__ = 'bank_pb2'
    # @@protoc_insertion_point(class_scope:bank.Balances.AmountsEntry)
    ))
  ,
  DESCRIPTOR = _BALANCES,
  __module__ = 'bank_pb2'
  # @@protoc_insertion_point(class_scope:bank.Balances)
  ))
_sym_db.RegisterMessage(Balances)
_sym_db.RegisterMessage(Balances.AmountsEntry)

AccountsBalancesRequest = _reflection.GeneratedProtocolMessageType('AccountsBalancesRequest', (_message.Message,), dict(
  DESCRIPTOR = _ACCOUNTSBALANCESREQUEST,
  __module__ = 'bank_pb2'
  # @@protoc_insertion_point(class_scope:bank.AccountsBalancesRequest)
  ))
_sym_db.RegisterMessage(AccountsBalancesRequest)

AccountsBalancesResponse = _reflection.GeneratedProtocolMessageType('AccountsBalancesResponse', (_message.Message,), dict(

  BalancesEntry = _reflection.GeneratedProtocolMessageType('BalancesEntry', (_message.Message,), dict(
    DESCRIPTOR = _ACCOUNTSBALANCESRESPONSE_BALANCESENTRY,
    __module__ = 'bank_pb2'
    # @@protoc_insertion_point(class_scope:bank.AccountsBalancesResponse.BalancesEntry)
    ))
  ,
  DESCRIPTOR = _ACCOUNTSBALANCESRESPONSE,
  __module__ = 'bank_pb2'
  # @@protoc_insertion_point(class_scope:bank.AccountsBalancesResponse)
  ))
_sym_db.RegisterMessage(AccountsBalancesResponse)
_sym_db.RegisterMessage(AccountsBalancesResponse.BalancesEntry)

AccountHistoryRequest = _reflection.GeneratedProtocolMessageType('AccountHistoryRequest', (_message.Message,), dict(
  DESCRIPTOR = _ACCOUNTHISTORYREQUEST,
  __module__ = 'bank_pb2'
  # @@protoc_insertion_point(class_scope:bank.AccountHistoryRequest)
  ))
_sym_db.RegisterMessage(AccountHistoryRequest)

AccountHistoryResponse = _reflection.GeneratedProtocolMessageType('AccountHistoryResponse', (_message.Message,), dict(
  DESCRIPTOR = _ACCOUNTHISTORYRESPONSE,
  __module__ = 'bank_pb2'
  # @@protoc_insertion_point(class_scope:bank.AccountHistoryResponse)
  ))
_sym_db.RegisterMessage(AccountHistoryResponse)

StartTransactionRequest = _reflection.GeneratedProtocolMessageType('StartTransactionRequest', (_message.Message,), dict(
  DESCRIPTOR = _STARTTRANSACTIONREQUEST,
  __module__ = 'bank_pb2'
  # @@protoc_insertion_point(class_scope:bank.StartTransactionRequest)
  ))
_sym_db.RegisterMessage(StartTransactionRequest)

StartTransactionResponse = _reflection.GeneratedProtocolMessageType('StartTransactionResponse', (_message.Message,), dict(
  DESCRIPTOR = _STARTTRANSACTIONRESPONSE,
  __module__ = 'bank_pb2'
  # @@protoc_insertion_point(class_scope:bank.StartTransactionResponse)
  ))
_sym_db.RegisterMessage(StartTransactionResponse)

CommitTransactionRequest = _reflection.GeneratedProtocolMessageType('CommitTransactionRequest', (_message.Message,), dict(
  DESCRIPTOR = _COMMITTRANSACTIONREQUEST,
  __module__ = 'bank_pb2'
  # @@protoc_insertion_point(class_scope:bank.CommitTransactionRequest)
  ))
_sym_db.RegisterMessage(CommitTransactionRequest)

CommitTransactionResponse = _reflection.GeneratedProtocolMessageType('CommitTransactionResponse', (_message.Message,), dict(
  DESCRIPTOR = _COMMITTRANSACTIONRESPONSE,
  __module__ = 'bank_pb2'
  # @@protoc_insertion_point(class_scope:bank.CommitTransactionResponse)
  ))
_sym_db.RegisterMessage(CommitTransactionResponse)

RollbackTransactionRequest = _reflection.GeneratedProtocolMessageType('RollbackTransactionRequest', (_message.Message,), dict(
  DESCRIPTOR = _ROLLBACKTRANSACTIONREQUEST,
  __module__ = 'bank_pb2'
  # @@protoc_insertion_point(class_scope:bank.RollbackTransactionRequest)
  ))
_sym_db.RegisterMessage(RollbackTransactionRequest)

RollbackTransactionResponse = _reflection.GeneratedProtocolMessageType('RollbackTransactionResponse', (_message.Message,), dict(
  DESCRIPTOR = _ROLLBACKTRANSACTIONRESPONSE,
  __module__ = 'bank_pb2'
  # @@protoc_insertion_point(class_scope:bank.RollbackTransactionResponse)
  ))
_sym_db.RegisterMessage(RollbackTransactionResponse)

DebugClearServiceRequest = _reflection.GeneratedProtocolMessageType('DebugClearServiceRequest', (_message.Message,), dict(
  DESCRIPTOR = _DEBUGCLEARSERVICEREQUEST,
  __module__ = 'bank_pb2'
  # @@protoc_insertion_point(class_scope:bank.DebugClearServiceRequest)
  ))
_sym_db.RegisterMessage(DebugClearServiceRequest)

DebugClearServiceResponse = _reflection.GeneratedProtocolMessageType('DebugClearServiceResponse', (_message.Message,), dict(
  DESCRIPTOR = _DEBUGCLEARSERVICERESPONSE,
  __module__ = 'bank_pb2'
  # @@protoc_insertion_point(class_scope:bank.DebugClearServiceResponse)
  ))
_sym_db.RegisterMessage(DebugClearServiceResponse)


_BALANCES_AMOUNTSENTRY.has_options = True
_BALANCES_AMOUNTSENTRY._options = _descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001'))
_ACCOUNTSBALANCESRESPONSE_BALANCESENTRY.has_options = True
_ACCOUNTSBALANCESRESPONSE_BALANCESENTRY._options = _descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001'))
# @@protoc_insertion_point(module_scope)
