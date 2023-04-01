# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: response.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eresponse.proto\"}\n\x0cUpdatedTitle\x12\x15\n\x05title\x18\x01 \x01(\x0b\x32\x06.Title\x12\x12\n\nchapter_id\x18\x02 \x01(\r\x12\x14\n\x0c\x63hapter_name\x18\x03 \x01(\t\x12\x19\n\x11\x63hapter_sub_title\x18\x04 \x01(\t\x12\x11\n\tis_latest\x18\x05 \x01(\x08\"2\n\x11UpdatedTitleGroup\x12\x1d\n\x06titles\x18\x02 \x03(\x0b\x32\r.UpdatedTitle\"1\n\x0bWebHomeView\x12\"\n\x06groups\x18\x02 \x03(\x0b\x32\x12.UpdatedTitleGroup\"&\n\x05Popup\x12\x0f\n\x07subject\x18\x01 \x01(\t\x12\x0c\n\x04\x62ody\x18\x02 \x01(\t\"\xcd\x01\n\x05Title\x12\x10\n\x08title_id\x18\x01 \x01(\r\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x03 \x01(\t\x12\x1a\n\x12portrait_image_url\x18\x04 \x01(\t\x12\x1b\n\x13landscape_image_url\x18\x05 \x01(\t\x12\x12\n\nview_count\x18\x06 \x01(\r\x12!\n\x08language\x18\x07 \x01(\x0e\x32\x0f.Title.Language\"$\n\x08Language\x12\x0b\n\x07\x45NGLISH\x10\x00\x12\x0b\n\x07SPANISH\x10\x01\"\x97\x01\n\x07\x43hapter\x12\x10\n\x08title_id\x18\x01 \x01(\r\x12\x12\n\nchapter_id\x18\x02 \x01(\r\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x11\n\tsub_title\x18\x04 \x01(\t\x12\x15\n\rthumbnail_url\x18\x05 \x01(\t\x12\x17\n\x0fstart_timestamp\x18\x06 \x01(\r\x12\x15\n\rend_timestamp\x18\x07 \x01(\r\"\xe8\x03\n\x0fTitleDetailView\x12\x15\n\x05title\x18\x01 \x01(\x0b\x32\x06.Title\x12\x17\n\x0ftitle_image_url\x18\x02 \x01(\t\x12\x10\n\x08overview\x18\x03 \x01(\t\x12\x1c\n\x14\x62\x61\x63kground_image_url\x18\x04 \x01(\t\x12\x16\n\x0enext_timestamp\x18\x05 \x01(\r\x12\x34\n\rupdate_timing\x18\x06 \x01(\x0e\x32\x1d.TitleDetailView.UpdateTiming\x12\"\n\x1aviewing_period_description\x18\x07 \x01(\t\x12\x1b\n\x13non_appearance_info\x18\x08 \x01(\t\x12\"\n\x12recommended_titles\x18\x0c \x03(\x0b\x32\x06.Title\x12\x18\n\x10is_simul_release\x18\x0e \x01(\x08\x12\x1f\n\x08\x63hapters\x18\x1c \x01(\x0b\x32\r.ChaptersView\"\x86\x01\n\x0cUpdateTiming\x12\x11\n\rNOT_REGULARLY\x10\x00\x12\n\n\x06MONDAY\x10\x01\x12\x0b\n\x07TUESDAY\x10\x02\x12\r\n\tWEDNESDAY\x10\x03\x12\x0c\n\x08THURSDAY\x10\x04\x12\n\n\x06\x46RIDAY\x10\x05\x12\x0c\n\x08SATURDAY\x10\x06\x12\n\n\x06SUNDAY\x10\x07\x12\x07\n\x03\x44\x41Y\x10\x08\"\x85\x01\n\x0c\x43haptersView\x12$\n\x12\x66irst_chapter_list\x18\x02 \x03(\x0b\x32\x08.Chapter\x12*\n\x18unavailable_chapter_list\x18\x03 \x03(\x0b\x32\x08.Chapter\x12#\n\x11last_chapter_list\x18\x04 \x03(\x0b\x32\x08.Chapter\"4\n\rTitleVariants\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x15\n\x05title\x18\x02 \x03(\x0b\x32\x06.Title\"7\n\rAllTitlesView\x12&\n\x0etitle_variants\x18\x01 \x03(\x0b\x32\x0e.TitleVariants\"\x90\x01\n\rSuccessResult\x12(\n\x0ctitle_detail\x18\x08 \x01(\x0b\x32\x10.TitleDetailViewH\x00\x12%\n\rweb_home_view\x18\x0b \x01(\x0b\x32\x0c.WebHomeViewH\x00\x12$\n\nall_titles\x18\x19 \x01(\x0b\x32\x0e.AllTitlesViewH\x00\x42\x08\n\x06result\"x\n\x0b\x45rrorResult\x12\x17\n\x06\x61\x63tion\x18\x01 \x01(\x0e\x32\x07.Action\x12\x1d\n\renglish_popup\x18\x02 \x01(\x0b\x32\x06.Popup\x12\x1d\n\rspanish_popup\x18\x03 \x01(\x0b\x32\x06.Popup\x12\x12\n\ndebug_info\x18\x04 \x01(\t\"V\n\x08Response\x12&\n\x0esuccess_result\x18\x01 \x01(\x0b\x32\x0e.SuccessResult\x12\"\n\x0c\x65rror_result\x18\x02 \x01(\x0b\x32\x0c.ErrorResult*L\n\x06\x41\x63tion\x12\x0b\n\x07\x44\x45\x46\x41ULT\x10\x00\x12\x10\n\x0cUNAUTHORIZED\x10\x01\x12\x0f\n\x0bMAINTENANCE\x10\x02\x12\x12\n\x0eGEOIP_BLOCKING\x10\x03\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'response_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_ACTION']._serialized_start=1745
  _globals['_ACTION']._serialized_end=1821
  _globals['_UPDATEDTITLE']._serialized_start=18
  _globals['_UPDATEDTITLE']._serialized_end=143
  _globals['_UPDATEDTITLEGROUP']._serialized_start=145
  _globals['_UPDATEDTITLEGROUP']._serialized_end=195
  _globals['_WEBHOMEVIEW']._serialized_start=197
  _globals['_WEBHOMEVIEW']._serialized_end=246
  _globals['_POPUP']._serialized_start=248
  _globals['_POPUP']._serialized_end=286
  _globals['_TITLE']._serialized_start=289
  _globals['_TITLE']._serialized_end=494
  _globals['_TITLE_LANGUAGE']._serialized_start=458
  _globals['_TITLE_LANGUAGE']._serialized_end=494
  _globals['_CHAPTER']._serialized_start=497
  _globals['_CHAPTER']._serialized_end=648
  _globals['_TITLEDETAILVIEW']._serialized_start=651
  _globals['_TITLEDETAILVIEW']._serialized_end=1139
  _globals['_TITLEDETAILVIEW_UPDATETIMING']._serialized_start=1005
  _globals['_TITLEDETAILVIEW_UPDATETIMING']._serialized_end=1139
  _globals['_CHAPTERSVIEW']._serialized_start=1142
  _globals['_CHAPTERSVIEW']._serialized_end=1275
  _globals['_TITLEVARIANTS']._serialized_start=1277
  _globals['_TITLEVARIANTS']._serialized_end=1329
  _globals['_ALLTITLESVIEW']._serialized_start=1331
  _globals['_ALLTITLESVIEW']._serialized_end=1386
  _globals['_SUCCESSRESULT']._serialized_start=1389
  _globals['_SUCCESSRESULT']._serialized_end=1533
  _globals['_ERRORRESULT']._serialized_start=1535
  _globals['_ERRORRESULT']._serialized_end=1655
  _globals['_RESPONSE']._serialized_start=1657
  _globals['_RESPONSE']._serialized_end=1743
# @@protoc_insertion_point(module_scope)