# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: classeur.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='classeur.proto',
  package='classeur',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0e\x63lasseur.proto\x12\x08\x63lasseur\"5\n\x0fUserCredentials\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"\x1d\n\x08Validity\x12\x11\n\tvailidity\x18\x01 \x01(\x08\"\x1d\n\tUserToken\x12\x10\n\x08username\x18\x01 \x01(\t\"\x18\n\x08\x46ileSize\x12\x0c\n\x04size\x18\x01 \x01(\x03\"2\n\x08\x46ileList\x12\x12\n\nfilesOwned\x18\x01 \x01(\t\x12\x12\n\nfilesSizes\x18\x02 \x01(\x03\"T\n\nFileChunks\x12\x10\n\x08\x66ileName\x18\x01 \x01(\t\x12\x0f\n\x07\x63hunkId\x18\x02 \x01(\x03\x12\x11\n\tchunkData\x18\x03 \x01(\t\x12\x10\n\x08userName\x18\x04 \x01(\t\"1\n\x0c\x43hunkDetails\x12\x10\n\x08\x66ileName\x18\x01 \x01(\t\x12\x0f\n\x07\x63hunkId\x18\x02 \x01(\x03\"#\n\x0f\x41\x63knowledgement\x12\x10\n\x08response\x18\x01 \x01(\x08\".\n\x08\x46ileName\x12\x10\n\x08\x66ileName\x18\x01 \x01(\t\x12\x10\n\x08userName\x18\x02 \x01(\t\"\x1a\n\x07Request\x12\x0f\n\x07request\x18\x01 \x01(\t\"\x1c\n\x08Response\x12\x10\n\x08response\x18\x02 \x01(\t\"4\n\x0cSNodeDetails\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x03\x12\n\n\x02id\x18\x03 \x01(\t2\xc9\x02\n\rclientHandler\x12\x46\n\x13\x43heckAuthentication\x12\x19.classeur.UserCredentials\x1a\x12.classeur.Validity\"\x00\x12\x36\n\tListFiles\x12\x13.classeur.UserToken\x1a\x12.classeur.FileList\"\x00\x12\x41\n\nUploadFile\x12\x14.classeur.FileChunks\x1a\x19.classeur.Acknowledgement\"\x00(\x01\x12<\n\x0c\x44ownloadFile\x12\x12.classeur.FileName\x1a\x14.classeur.FileChunks\"\x00\x30\x01\x12\x37\n\nReportSize\x12\x13.classeur.UserToken\x1a\x12.classeur.FileSize\"\x00\x32\x96\x01\n\x0csNodeHandler\x12\x45\n\x0eSendFileChunks\x12\x14.classeur.FileChunks\x1a\x19.classeur.Acknowledgement\"\x00(\x01\x12?\n\x08\x41\x64\x64SNode\x12\x16.classeur.SNodeDetails\x1a\x19.classeur.Acknowledgement\"\x00\x62\x06proto3')
)




_USERCREDENTIALS = _descriptor.Descriptor(
  name='UserCredentials',
  full_name='classeur.UserCredentials',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='username', full_name='classeur.UserCredentials.username', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='password', full_name='classeur.UserCredentials.password', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=28,
  serialized_end=81,
)


_VALIDITY = _descriptor.Descriptor(
  name='Validity',
  full_name='classeur.Validity',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='vailidity', full_name='classeur.Validity.vailidity', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=83,
  serialized_end=112,
)


_USERTOKEN = _descriptor.Descriptor(
  name='UserToken',
  full_name='classeur.UserToken',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='username', full_name='classeur.UserToken.username', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=114,
  serialized_end=143,
)


_FILESIZE = _descriptor.Descriptor(
  name='FileSize',
  full_name='classeur.FileSize',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='size', full_name='classeur.FileSize.size', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=145,
  serialized_end=169,
)


_FILELIST = _descriptor.Descriptor(
  name='FileList',
  full_name='classeur.FileList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='filesOwned', full_name='classeur.FileList.filesOwned', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='filesSizes', full_name='classeur.FileList.filesSizes', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=171,
  serialized_end=221,
)


_FILECHUNKS = _descriptor.Descriptor(
  name='FileChunks',
  full_name='classeur.FileChunks',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fileName', full_name='classeur.FileChunks.fileName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='chunkId', full_name='classeur.FileChunks.chunkId', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='chunkData', full_name='classeur.FileChunks.chunkData', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='userName', full_name='classeur.FileChunks.userName', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=223,
  serialized_end=307,
)


_CHUNKDETAILS = _descriptor.Descriptor(
  name='ChunkDetails',
  full_name='classeur.ChunkDetails',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fileName', full_name='classeur.ChunkDetails.fileName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='chunkId', full_name='classeur.ChunkDetails.chunkId', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=309,
  serialized_end=358,
)


_ACKNOWLEDGEMENT = _descriptor.Descriptor(
  name='Acknowledgement',
  full_name='classeur.Acknowledgement',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='response', full_name='classeur.Acknowledgement.response', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=360,
  serialized_end=395,
)


_FILENAME = _descriptor.Descriptor(
  name='FileName',
  full_name='classeur.FileName',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fileName', full_name='classeur.FileName.fileName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='userName', full_name='classeur.FileName.userName', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=397,
  serialized_end=443,
)


_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='classeur.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='request', full_name='classeur.Request.request', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=445,
  serialized_end=471,
)


_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='classeur.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='response', full_name='classeur.Response.response', index=0,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=473,
  serialized_end=501,
)


_SNODEDETAILS = _descriptor.Descriptor(
  name='SNodeDetails',
  full_name='classeur.SNodeDetails',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ip', full_name='classeur.SNodeDetails.ip', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port', full_name='classeur.SNodeDetails.port', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='classeur.SNodeDetails.id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=503,
  serialized_end=555,
)

DESCRIPTOR.message_types_by_name['UserCredentials'] = _USERCREDENTIALS
DESCRIPTOR.message_types_by_name['Validity'] = _VALIDITY
DESCRIPTOR.message_types_by_name['UserToken'] = _USERTOKEN
DESCRIPTOR.message_types_by_name['FileSize'] = _FILESIZE
DESCRIPTOR.message_types_by_name['FileList'] = _FILELIST
DESCRIPTOR.message_types_by_name['FileChunks'] = _FILECHUNKS
DESCRIPTOR.message_types_by_name['ChunkDetails'] = _CHUNKDETAILS
DESCRIPTOR.message_types_by_name['Acknowledgement'] = _ACKNOWLEDGEMENT
DESCRIPTOR.message_types_by_name['FileName'] = _FILENAME
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Response'] = _RESPONSE
DESCRIPTOR.message_types_by_name['SNodeDetails'] = _SNODEDETAILS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UserCredentials = _reflection.GeneratedProtocolMessageType('UserCredentials', (_message.Message,), dict(
  DESCRIPTOR = _USERCREDENTIALS,
  __module__ = 'classeur_pb2'
  # @@protoc_insertion_point(class_scope:classeur.UserCredentials)
  ))
_sym_db.RegisterMessage(UserCredentials)

Validity = _reflection.GeneratedProtocolMessageType('Validity', (_message.Message,), dict(
  DESCRIPTOR = _VALIDITY,
  __module__ = 'classeur_pb2'
  # @@protoc_insertion_point(class_scope:classeur.Validity)
  ))
_sym_db.RegisterMessage(Validity)

UserToken = _reflection.GeneratedProtocolMessageType('UserToken', (_message.Message,), dict(
  DESCRIPTOR = _USERTOKEN,
  __module__ = 'classeur_pb2'
  # @@protoc_insertion_point(class_scope:classeur.UserToken)
  ))
_sym_db.RegisterMessage(UserToken)

FileSize = _reflection.GeneratedProtocolMessageType('FileSize', (_message.Message,), dict(
  DESCRIPTOR = _FILESIZE,
  __module__ = 'classeur_pb2'
  # @@protoc_insertion_point(class_scope:classeur.FileSize)
  ))
_sym_db.RegisterMessage(FileSize)

FileList = _reflection.GeneratedProtocolMessageType('FileList', (_message.Message,), dict(
  DESCRIPTOR = _FILELIST,
  __module__ = 'classeur_pb2'
  # @@protoc_insertion_point(class_scope:classeur.FileList)
  ))
_sym_db.RegisterMessage(FileList)

FileChunks = _reflection.GeneratedProtocolMessageType('FileChunks', (_message.Message,), dict(
  DESCRIPTOR = _FILECHUNKS,
  __module__ = 'classeur_pb2'
  # @@protoc_insertion_point(class_scope:classeur.FileChunks)
  ))
_sym_db.RegisterMessage(FileChunks)

ChunkDetails = _reflection.GeneratedProtocolMessageType('ChunkDetails', (_message.Message,), dict(
  DESCRIPTOR = _CHUNKDETAILS,
  __module__ = 'classeur_pb2'
  # @@protoc_insertion_point(class_scope:classeur.ChunkDetails)
  ))
_sym_db.RegisterMessage(ChunkDetails)

Acknowledgement = _reflection.GeneratedProtocolMessageType('Acknowledgement', (_message.Message,), dict(
  DESCRIPTOR = _ACKNOWLEDGEMENT,
  __module__ = 'classeur_pb2'
  # @@protoc_insertion_point(class_scope:classeur.Acknowledgement)
  ))
_sym_db.RegisterMessage(Acknowledgement)

FileName = _reflection.GeneratedProtocolMessageType('FileName', (_message.Message,), dict(
  DESCRIPTOR = _FILENAME,
  __module__ = 'classeur_pb2'
  # @@protoc_insertion_point(class_scope:classeur.FileName)
  ))
_sym_db.RegisterMessage(FileName)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(
  DESCRIPTOR = _REQUEST,
  __module__ = 'classeur_pb2'
  # @@protoc_insertion_point(class_scope:classeur.Request)
  ))
_sym_db.RegisterMessage(Request)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), dict(
  DESCRIPTOR = _RESPONSE,
  __module__ = 'classeur_pb2'
  # @@protoc_insertion_point(class_scope:classeur.Response)
  ))
_sym_db.RegisterMessage(Response)

SNodeDetails = _reflection.GeneratedProtocolMessageType('SNodeDetails', (_message.Message,), dict(
  DESCRIPTOR = _SNODEDETAILS,
  __module__ = 'classeur_pb2'
  # @@protoc_insertion_point(class_scope:classeur.SNodeDetails)
  ))
_sym_db.RegisterMessage(SNodeDetails)



_CLIENTHANDLER = _descriptor.ServiceDescriptor(
  name='clientHandler',
  full_name='classeur.clientHandler',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=558,
  serialized_end=887,
  methods=[
  _descriptor.MethodDescriptor(
    name='CheckAuthentication',
    full_name='classeur.clientHandler.CheckAuthentication',
    index=0,
    containing_service=None,
    input_type=_USERCREDENTIALS,
    output_type=_VALIDITY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='ListFiles',
    full_name='classeur.clientHandler.ListFiles',
    index=1,
    containing_service=None,
    input_type=_USERTOKEN,
    output_type=_FILELIST,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='UploadFile',
    full_name='classeur.clientHandler.UploadFile',
    index=2,
    containing_service=None,
    input_type=_FILECHUNKS,
    output_type=_ACKNOWLEDGEMENT,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='DownloadFile',
    full_name='classeur.clientHandler.DownloadFile',
    index=3,
    containing_service=None,
    input_type=_FILENAME,
    output_type=_FILECHUNKS,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='ReportSize',
    full_name='classeur.clientHandler.ReportSize',
    index=4,
    containing_service=None,
    input_type=_USERTOKEN,
    output_type=_FILESIZE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_CLIENTHANDLER)

DESCRIPTOR.services_by_name['clientHandler'] = _CLIENTHANDLER


_SNODEHANDLER = _descriptor.ServiceDescriptor(
  name='sNodeHandler',
  full_name='classeur.sNodeHandler',
  file=DESCRIPTOR,
  index=1,
  serialized_options=None,
  serialized_start=890,
  serialized_end=1040,
  methods=[
  _descriptor.MethodDescriptor(
    name='SendFileChunks',
    full_name='classeur.sNodeHandler.SendFileChunks',
    index=0,
    containing_service=None,
    input_type=_FILECHUNKS,
    output_type=_ACKNOWLEDGEMENT,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='AddSNode',
    full_name='classeur.sNodeHandler.AddSNode',
    index=1,
    containing_service=None,
    input_type=_SNODEDETAILS,
    output_type=_ACKNOWLEDGEMENT,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_SNODEHANDLER)

DESCRIPTOR.services_by_name['sNodeHandler'] = _SNODEHANDLER

# @@protoc_insertion_point(module_scope)
