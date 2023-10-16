from globals import config

assembly_path = config.MTGA_folder + r"/MTGA_Data/Managed/"

import sys
sys.path.append(assembly_path)

import clr
clr.AddReference("Wizards.Mtga.Metadata")
clr.AddReference("Assembly-CSharp")
clr.AddReference("Wizards.MDN.GreProtobuf.Unity")
clr.AddReference("Google.Protobuf")

import Wotc.Mtgo.Gre.External.Messaging as gre # C# classes under namespace 'Wotc.Mtgo.Gre.External.Messaging'
import message_pb2 as pb # python classes genereated with protobuf compiler