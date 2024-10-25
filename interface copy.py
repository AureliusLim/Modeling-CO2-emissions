import numpy as np
import traci
import xml.etree.ElementTree as ET
import joblib
from rtree import index
from jinja2 import Template

template = Template('''<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">
  
    
    <!-- Routes --><route id="r_1" edges="29377703#0 29377703#1 29377703#2 29377703#3 29377703#4 303412427#0 303412427#1 303412427#2 303412427#3 303412427#4 303412427#5 303412427#6 303412427#7 303412427#8 303412427#9 303412427#10 303412427#11 303412427#12 303412427#13 303412427#14 303412427#15 303412427#16 303412427#17 303412427#18 303412427#19 924607338 924607337#0 924607337#1 924607337#2 924607337#3 924607337#4 615456195 615456193#0 615456193#1 615456193#2 615478345 615478344#0 615478344#1 368461882#0 368461882#1 368461882#2 694268908 923261416 694268909#0 694268909#1 1176045778 82694445#0 82694445#1 82694445#2 1176045777 82694458#0 82694458#1 575729552#0 575729552#1 4086429 4332731 745183365#0 -575729108#4 -575729108#3 -575729108#2 -575729108#1 -575729555 -940627086 -4332734#7 -4332734#6 -4332734#5 -4332734#4 -4332734#3 -4332734#2 -4332734#1 -4332734#0 -4478182 -48630242#3 -48630242#2 -48630242#1 4243614#1 685156794#0 685156794#1 706706674#0 820063579#0 820063579#1 107396681#0 107396681#4 107396681#5 107396681#6 107396681#7 1148489399#0 1148489399#1 1148489399#2 1018627463 -1076442002 -4588647#5 -4588647#4 -4588647#3 -4588647#0 -917450542 1174874706 1182394700 136822582 1174874705 161754856 917450546#0 917450546#2 4637649 1158575268 1156612124 161754854#0 161754854#1 161754854#2 136822571#1 136822571#2 136822571#3 136822574 136822584 369686026 121188635 332624272 126342419 757990549 1074607189#0 1074607189#1 119883577#1 119883577#4 119883577#5 119883577#6 119883577#7 119883577#8 119883577#9 119883577#10 5019952#0 5019952#1 5019952#2 5019952#4 5019952#5 825090426 704746733#0 -187486758#5 -187486758#1 -187486758#0 16174062#0 16174062#1 16174062#2 16174062#3 16174062#4 16174062#5 176435849 820063585 -178615165 820063587#0 820063587#1 176435850 176435844#0 176435844#1 176435844#3 176435844#4 176435844#5 176435844#6 176435844#7 820063588 820063582#0 820063582#1 945948203 54338767#0 54338767#1 54338767#2 1072039865#1 704746731#0 704746731#2 704746731#3 1171640558 20816626#0 20816626#1 310627474#0 310627474#1 310627474#2 310627474#3 310627474#4 310627474#7 1074607188 940612553 757990561 121188638 126342421 136822570 757990562 136822575 136822580#0 136822580#1 136822580#2 136822580#3 295073752#0 136822587#0 136822587#1 136822587#2 136822587#3 161754855#0 161754855#1 917450547#0 917450547#2 402897988#1 32981461 917450545 1112806233-AddedOnRampEdge 1112806233 4588647#0 4588647#3 4588647#4 4588647#5 1076442002 1018627464 4258656#0 4258656#1 4258656#2 4258656#4 729164042#1 805198994#0 805198994#1 329609972#0 329609972#1 729164041#0 729164041#1 820063578#0 820063578#1 48630242#1 48630242#2 48630242#3 4478182 4332734#0 4332734#1 4332734#2 4332734#3 4332734#4 4332734#5 4332734#6 4332734#7 940627086 575729555 575729108#1 575729108#2 575729108#3 575729108#4 745183363 745183362 745183364#0 745183364#1 745183364#2 -82694458#1 -82694458#0 -1176045777 -82694445#2 -82694445#1 -82694445#0 -1176045778 -694268909#1 -694268909#0 -923261416 -694268908 -368461882#2 -368461882#1 -368461882#0 -615478344#1 -615478344#0 -615478345 -615456193#2 -615456193#1 -615456193#0 154644778#0 154644778#1 -924607337#4 -924607337#3 -924607337#2 -924607337#1 -924607337#0 -924607338 -303412427#19 -303412427#18 -303412427#17 -303412427#16 -303412427#15 -303412427#14 -303412427#13 -303412427#12 -303412427#11 -303412427#10 -303412427#9 -303412427#8 -303412427#7 -303412427#6 -303412427#5 -303412427#4 -303412427#3 -303412427#2 -303412427#1 -303412427#0 -29377703#4 -29377703#3 -29377703#2 -29377703#1 -29377703#0 -1069829005#2 -1069829005#1 1069829005#1 1069829005#2 29377703#0 29377703#1 29377703#2 29377703#3 29377703#4 303412427#0 303412427#1 303412427#2 303412427#3 303412427#4 303412427#5 303412427#6 303412427#7 303412427#8 303412427#9 303412427#10 303412427#11 303412427#12 303412427#13 303412427#14 303412427#15 303412427#16 303412427#17 303412427#18 303412427#19 924607338 924607337#0 924607337#1 924607337#2 924607337#3 924607337#4 615456195 615456193#0 615456193#1 615456193#2 615478345 615478344#0 615478344#1 368461882#0 368461882#1 368461882#2 694268908 923261416 694268909#0 694268909#1 1176045778 82694445#0 82694445#1 82694445#2 1176045777 82694458#0 82694458#1 575729552#0 575729552#1 4086429 4332731 745183365#0 -575729108#4 -575729108#3 -575729108#2 -575729108#1 -575729555 -940627086 -4332734#7 -4332734#6 -4332734#5 -4332734#4 -4332734#3 -4332734#2 -4332734#1 -4332734#0 -4478182 -48630242#3 -48630242#2 -48630242#1 4243614#1 685156794#0 685156794#1 706706674#0 820063579#0 820063579#1 107396681#0 107396681#4 107396681#5 107396681#6 107396681#7 1148489399#0 1148489399#1 1148489399#2 1018627463 -1076442002 -4588647#5 -4588647#4 -4588647#3 -4588647#0 -917450542 1174874706 1182394700 136822582 1174874705 161754856 917450546#0 917450546#2 4637649 1158575268 1156612124 161754854#0 161754854#1 161754854#2 136822571#1 136822571#2 136822571#3 136822574 136822584 369686026 121188635 332624272 126342419 757990549 1074607189#0 1074607189#1 119883577#1 119883577#4 119883577#5 119883577#6 119883577#7 119883577#8 119883577#9 119883577#10 5019952#0 5019952#1 5019952#2 5019952#4 5019952#5 825090426 704746733#0 -187486758#5 -187486758#1 -187486758#0 16174062#0 16174062#1 16174062#2 16174062#3 16174062#4 16174062#5 176435849 820063585 -178615165 820063587#0 820063587#1 176435850 176435844#0 176435844#1 176435844#3 176435844#4 176435844#5 176435844#6 176435844#7 820063588 820063582#0 820063582#1 945948203 54338767#0 54338767#1 54338767#2 1072039865#1 704746731#0 704746731#2 704746731#3 1171640558 20816626#0 20816626#1 310627474#0 310627474#1 310627474#2 310627474#3 310627474#4 310627474#7 1074607188 940612553 757990561 121188638 126342421 136822570 757990562 136822575 136822580#0 136822580#1 136822580#2 136822580#3 295073752#0 136822587#0 136822587#1 136822587#2 136822587#3 161754855#0 161754855#1 917450547#0 917450547#2 402897988#1 32981461 917450545 1112806233-AddedOnRampEdge 1112806233 4588647#0 4588647#3 4588647#4 4588647#5 1076442002 1018627464 4258656#0 4258656#1 4258656#2 4258656#4 729164042#1 805198994#0 805198994#1 329609972#0 329609972#1 729164041#0 729164041#1 820063578#0 820063578#1 48630242#1 48630242#2 48630242#3 4478182 4332734#0 4332734#1 4332734#2 4332734#3 4332734#4 4332734#5 4332734#6 4332734#7 940627086 575729555 575729108#1 575729108#2 575729108#3 575729108#4 745183363 745183362 745183364#0 745183364#1 745183364#2 -82694458#1 -82694458#0 -1176045777 -82694445#2 -82694445#1 -82694445#0 -1176045778 -694268909#1 -694268909#0 -923261416 -694268908 -368461882#2 -368461882#1 -368461882#0 -615478344#1 -615478344#0 -615478345 -615456193#2 -615456193#1 -615456193#0 154644778#0 154644778#1 -924607337#4 -924607337#3 -924607337#2 -924607337#1 -924607337#0 -924607338 -303412427#19 -303412427#18 -303412427#17 -303412427#16 -303412427#15 -303412427#14 -303412427#13 -303412427#12 -303412427#11 -303412427#10 -303412427#9 -303412427#8 -303412427#7 -303412427#6 -303412427#5 -303412427#4 -303412427#3 -303412427#2 -303412427#1 -303412427#0 -29377703#4 -29377703#3 -29377703#2 -29377703#1 -29377703#0 -1069829005#2 -1069829005#1 1069829005#1 1069829005#2 29377703#0 29377703#1 29377703#2 29377703#3 29377703#4 303412427#0 303412427#1 303412427#2 303412427#3 303412427#4 303412427#5 303412427#6 303412427#7 303412427#8 303412427#9 303412427#10 303412427#11 303412427#12 303412427#13 303412427#14 303412427#15 303412427#16 303412427#17 303412427#18 303412427#19 924607338 924607337#0 924607337#1 924607337#2 924607337#3 924607337#4 615456195 615456193#0 615456193#1 615456193#2 615478345 615478344#0 615478344#1 368461882#0 368461882#1 368461882#2 694268908 923261416 694268909#0 694268909#1 1176045778 82694445#0 82694445#1 82694445#2 1176045777 82694458#0 82694458#1 575729552#0 575729552#1 4086429 4332731 745183365#0 -575729108#4 -575729108#3 -575729108#2 -575729108#1 -575729555 -940627086 -4332734#7 -4332734#6 -4332734#5 -4332734#4 -4332734#3 -4332734#2 -4332734#1 -4332734#0 -4478182 -48630242#3 -48630242#2 -48630242#1 4243614#1 685156794#0 685156794#1 706706674#0 820063579#0 820063579#1 107396681#0 107396681#4 107396681#5 107396681#6 107396681#7 1148489399#0 1148489399#1 1148489399#2 1018627463 -1076442002 -4588647#5 -4588647#4 -4588647#3 -4588647#0 -917450542 1174874706 1182394700 136822582 1174874705 161754856 917450546#0 917450546#2 4637649 1158575268 1156612124 161754854#0 161754854#1 161754854#2 136822571#1 136822571#2 136822571#3 136822574 136822584 369686026 121188635 332624272 126342419 757990549 1074607189#0 1074607189#1 119883577#1 119883577#4 119883577#5 119883577#6 119883577#7 119883577#8 119883577#9 119883577#10 5019952#0 5019952#1 5019952#2 5019952#4 5019952#5 825090426 704746733#0 -187486758#5 -187486758#1 -187486758#0 16174062#0 16174062#1 16174062#2 16174062#3 16174062#4 16174062#5 176435849 820063585 -178615165 820063587#0 820063587#1 176435850 176435844#0 176435844#1 176435844#3 176435844#4 176435844#5 176435844#6 176435844#7 820063588 820063582#0 820063582#1 945948203 54338767#0 54338767#1 54338767#2 1072039865#1 704746731#0 704746731#2 704746731#3 1171640558 20816626#0 20816626#1 310627474#0 310627474#1 310627474#2 310627474#3 310627474#4 310627474#7 1074607188 940612553 757990561 121188638 126342421 136822570 757990562 136822575 136822580#0 136822580#1 136822580#2 136822580#3 295073752#0 136822587#0 136822587#1 136822587#2 136822587#3 161754855#0 161754855#1 917450547#0 917450547#2 402897988#1 32981461 917450545 1112806233-AddedOnRampEdge 1112806233 4588647#0 4588647#3 4588647#4 4588647#5 1076442002 1018627464 4258656#0 4258656#1 4258656#2 4258656#4 729164042#1 805198994#0 805198994#1 329609972#0 329609972#1 729164041#0 729164041#1 820063578#0 820063578#1 48630242#1 48630242#2 48630242#3 4478182 4332734#0 4332734#1 4332734#2 4332734#3 4332734#4 4332734#5 4332734#6 4332734#7 940627086 575729555 575729108#1 575729108#2 575729108#3 575729108#4 745183363 745183362 745183364#0 745183364#1 745183364#2 -82694458#1 -82694458#0 -1176045777 -82694445#2 -82694445#1 -82694445#0 -1176045778 -694268909#1 -694268909#0 -923261416 -694268908 -368461882#2 -368461882#1 -368461882#0 -615478344#1 -615478344#0 -615478345 -615456193#2 -615456193#1 -615456193#0 154644778#0 154644778#1 -924607337#4 -924607337#3 -924607337#2 -924607337#1 -924607337#0 -924607338 -303412427#19 -303412427#18 -303412427#17 -303412427#16 -303412427#15 -303412427#14 -303412427#13 -303412427#12 -303412427#11 -303412427#10 -303412427#9 -303412427#8 -303412427#7 -303412427#6 -303412427#5 -303412427#4 -303412427#3 -303412427#2 -303412427#1 -303412427#0 -29377703#4 -29377703#3 -29377703#2 -29377703#1 -29377703#0 -1069829005#2 -1069829005#1 1069829005#1 1069829005#2 29377703#0 29377703#1 29377703#2 29377703#3 29377703#4 303412427#0 303412427#1 303412427#2 303412427#3 303412427#4 303412427#5 303412427#6 303412427#7 303412427#8 303412427#9 303412427#10 303412427#11 303412427#12 303412427#13 303412427#14 303412427#15 303412427#16 303412427#17 303412427#18 303412427#19 924607338 924607337#0 924607337#1 924607337#2 924607337#3 924607337#4 615456195 615456193#0 615456193#1 615456193#2 615478345 615478344#0 615478344#1 368461882#0 368461882#1 368461882#2 694268908 923261416 694268909#0 694268909#1 1176045778 82694445#0 82694445#1 82694445#2 1176045777 82694458#0 82694458#1 575729552#0 575729552#1 4086429 4332731 745183365#0 -575729108#4 -575729108#3 -575729108#2 -575729108#1 -575729555 -940627086 -4332734#7 -4332734#6 -4332734#5 -4332734#4 -4332734#3 -4332734#2 -4332734#1 -4332734#0 -4478182 -48630242#3 -48630242#2 -48630242#1 4243614#1 685156794#0 685156794#1 706706674#0 820063579#0 820063579#1 107396681#0 107396681#4 107396681#5 107396681#6 107396681#7 1148489399#0 1148489399#1 1148489399#2 1018627463 -1076442002 -4588647#5 -4588647#4 -4588647#3 -4588647#0 -917450542 1174874706 1182394700 136822582 1174874705 161754856 917450546#0 917450546#2 4637649 1158575268 1156612124 161754854#0 161754854#1 161754854#2 136822571#1 136822571#2 136822571#3 136822574 136822584 369686026 121188635 332624272 126342419 757990549 1074607189#0 1074607189#1 119883577#1 119883577#4 119883577#5 119883577#6 119883577#7 119883577#8 119883577#9 119883577#10 5019952#0 5019952#1 5019952#2 5019952#4 5019952#5 825090426 704746733#0 -187486758#5 -187486758#1 -187486758#0 16174062#0 16174062#1 16174062#2 16174062#3 16174062#4 16174062#5 176435849 820063585 -178615165 820063587#0 820063587#1 176435850 176435844#0 176435844#1 176435844#3 176435844#4 176435844#5 176435844#6 176435844#7 820063588 820063582#0 820063582#1 945948203 54338767#0 54338767#1 54338767#2 1072039865#1 704746731#0 704746731#2 704746731#3 1171640558 20816626#0 20816626#1 310627474#0 310627474#1 310627474#2 310627474#3 310627474#4 310627474#7 1074607188 940612553 757990561 121188638 126342421 136822570 757990562 136822575 136822580#0 136822580#1 136822580#2 136822580#3 295073752#0 136822587#0 136822587#1 136822587#2 136822587#3 161754855#0 161754855#1 917450547#0 917450547#2 402897988#1 32981461 917450545 1112806233-AddedOnRampEdge 1112806233 4588647#0 4588647#3 4588647#4 4588647#5 1076442002 1018627464 4258656#0 4258656#1 4258656#2 4258656#4 729164042#1 805198994#0 805198994#1 329609972#0 329609972#1 729164041#0 729164041#1 820063578#0 820063578#1 48630242#1 48630242#2 48630242#3 4478182 4332734#0 4332734#1 4332734#2 4332734#3 4332734#4 4332734#5 4332734#6 4332734#7 940627086 575729555 575729108#1 575729108#2 575729108#3 575729108#4 745183363 745183362 745183364#0 745183364#1 745183364#2 -82694458#1 -82694458#0 -1176045777 -82694445#2 -82694445#1 -82694445#0 -1176045778 -694268909#1 -694268909#0 -923261416 -694268908 -368461882#2 -368461882#1 -368461882#0 -615478344#1 -615478344#0 -615478345 -615456193#2 -615456193#1 -615456193#0 154644778#0 154644778#1 -924607337#4 -924607337#3 -924607337#2 -924607337#1 -924607337#0 -924607338 -303412427#19 -303412427#18 -303412427#17 -303412427#16 -303412427#15 -303412427#14 -303412427#13 -303412427#12 -303412427#11 -303412427#10 -303412427#9 -303412427#8 -303412427#7 -303412427#6 -303412427#5 -303412427#4 -303412427#3 -303412427#2 -303412427#1 -303412427#0 -29377703#4 -29377703#3 -29377703#2 -29377703#1 -29377703#0 -1069829005#2 -1069829005#1 1069829005#1 1069829005#2 29377703#0 29377703#1 29377703#2 29377703#3 29377703#4 303412427#0 303412427#1 303412427#2 303412427#3 303412427#4 303412427#5 303412427#6 303412427#7 303412427#8 303412427#9 303412427#10 303412427#11 303412427#12 303412427#13 303412427#14 303412427#15 303412427#16 303412427#17 303412427#18 303412427#19 924607338 924607337#0 924607337#1 924607337#2 924607337#3 924607337#4 615456195 615456193#0 615456193#1 615456193#2 615478345 615478344#0 615478344#1 368461882#0 368461882#1 368461882#2 694268908 923261416 694268909#0 694268909#1 1176045778 82694445#0 82694445#1 82694445#2 1176045777 82694458#0 82694458#1 575729552#0 575729552#1 4086429 4332731 745183365#0 -575729108#4 -575729108#3 -575729108#2 -575729108#1 -575729555 -940627086 -4332734#7 -4332734#6 -4332734#5 -4332734#4 -4332734#3 -4332734#2 -4332734#1 -4332734#0 -4478182 -48630242#3 -48630242#2 -48630242#1 4243614#1 685156794#0 685156794#1 706706674#0 820063579#0 820063579#1 107396681#0 107396681#4 107396681#5 107396681#6 107396681#7 1148489399#0 1148489399#1 1148489399#2 1018627463 -1076442002 -4588647#5 -4588647#4 -4588647#3 -4588647#0 -917450542 1174874706 1182394700 136822582 1174874705 161754856 917450546#0 917450546#2 4637649 1158575268 1156612124 161754854#0 161754854#1 161754854#2 136822571#1 136822571#2 136822571#3 136822574 136822584 369686026 121188635 332624272 126342419 757990549 1074607189#0 1074607189#1 119883577#1 119883577#4 119883577#5 119883577#6 119883577#7 119883577#8 119883577#9 119883577#10 5019952#0 5019952#1 5019952#2 5019952#4 5019952#5 825090426 704746733#0 -187486758#5 -187486758#1 -187486758#0 16174062#0 16174062#1 16174062#2 16174062#3 16174062#4 16174062#5 176435849 820063585 -178615165 820063587#0 820063587#1 176435850 176435844#0 176435844#1 176435844#3 176435844#4 176435844#5 176435844#6 176435844#7 820063588 820063582#0 820063582#1 945948203 54338767#0 54338767#1 54338767#2 1072039865#1 704746731#0 704746731#2 704746731#3 1171640558 20816626#0 20816626#1 310627474#0 310627474#1 310627474#2 310627474#3 310627474#4 310627474#7 1074607188 940612553 757990561 121188638 126342421 136822570 757990562 136822575 136822580#0 136822580#1 136822580#2 136822580#3 295073752#0 136822587#0 136822587#1 136822587#2 136822587#3 161754855#0 161754855#1 917450547#0 917450547#2 402897988#1 32981461 917450545 1112806233-AddedOnRampEdge 1112806233 4588647#0 4588647#3 4588647#4 4588647#5 1076442002 1018627464 4258656#0 4258656#1 4258656#2 4258656#4 729164042#1 805198994#0 805198994#1 329609972#0 329609972#1 729164041#0 729164041#1 820063578#0 820063578#1 48630242#1 48630242#2 48630242#3 4478182 4332734#0 4332734#1 4332734#2 4332734#3 4332734#4 4332734#5 4332734#6 4332734#7 940627086 575729555 575729108#1 575729108#2 575729108#3 575729108#4 745183363 745183362 745183364#0 745183364#1 745183364#2 -82694458#1 -82694458#0 -1176045777 -82694445#2 -82694445#1 -82694445#0 -1176045778 -694268909#1 -694268909#0 -923261416 -694268908 -368461882#2 -368461882#1 -368461882#0 -615478344#1 -615478344#0 -615478345 -615456193#2 -615456193#1 -615456193#0 154644778#0 154644778#1 -924607337#4 -924607337#3 -924607337#2 -924607337#1 -924607337#0 -924607338 -303412427#19 -303412427#18 -303412427#17 -303412427#16 -303412427#15 -303412427#14 -303412427#13 -303412427#12 -303412427#11 -303412427#10 -303412427#9 -303412427#8 -303412427#7 -303412427#6 -303412427#5 -303412427#4 -303412427#3 -303412427#2 -303412427#1 -303412427#0 -29377703#4 -29377703#3 -29377703#2 -29377703#1 -29377703#0 -1069829005#2 -1069829005#1 1069829005#1 1069829005#2 "/>
    
    <!-- Vehicles, persons and containers (sorted by depart) -->
    
   
    {% for i in range(0, trad_count) %}
                    
    <vehicle id="jeepney_{{ i }}" type="traditional_jeepney" route="r_1" depart="0"/>
                    
    {% endfor %}
  
    {% for i in range(0, modern_count) %}
                    
    <vehicle id="modernjeepney_{{ i }}" type="modern_jeepney" route="r_1" depart="0"/>
                    
    {% endfor %}
                
                    

                    
</routes>    ''')
def modify_person_xml(file_path, trad_count, modern_count):
    # Parse the existing XML
    traditional_jeepneys = [f"jeepney_{i}" for i in range(trad_count)] 
    modern_jeepneys = [f"modernjeepney_{i}" for i in range(modern_count)]  

    # Combine into a single string with space separation
    all_jeepney_ids = " ".join(traditional_jeepneys + modern_jeepneys)
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Loop through all <person> elements
    for person in root.findall("person"):
        for ride in person.findall("ride"):
            # Modify the lines attribute to include all jeepney IDs
            ride.set("lines", all_jeepney_ids)

    # Save the modified XML back to the same file (or a new one if needed)
    tree.write(file_path, encoding="utf-8", xml_declaration=True)

def generate_routes_xml(trad_count, modern_count, output_file='jeepney_routes.rou.xml'):
    # Render the template with provided counts
    output = template.render(trad_count=trad_count, modern_count=modern_count)

    # Write the output to an XML file
    with open(output_file, 'w') as file:
        file.write(output)
    # Populate jeepney_id_list
    for i in range(0, trad_count):
        traditional_id_list.append(f'jeepney_{i}')
    for i in range(0, modern_count):
        modern_id_list.append(f'modernjeepney_{i}')
     
    print(f"{output_file} has been generated successfully.")


# Load the trained HMM model
trad_model = joblib.load('trained_hmm_model.pkl')
modern_model = joblib.load('trained_hmm_model_modern.pkl')
# Define state mappings
hidden_state_map = {'Vehicle': 0, 'Passenger': 1, 'Stoplight': 2}
observed_state_map = {'Go': 0, '1 Lane Right': 1, 'Load': 2, 'Stop': 3, '1 Lane Left': 4, 'Unload': 5, 'Wait': 6, '2 Lane Left': 7, '2 Lane Right': 8}

# Define reverse mappings for easy lookup
reverse_hidden_state_map = {v: k for k, v in hidden_state_map.items()}
reverse_observed_state_map = {v: k for k, v in observed_state_map.items()}
# Initialize the spatial index
spatial_index = index.Index()

def populate_spatial_index():
    for passenger_id in traci.person.getIDList():
        passenger_edge = traci.person.getRoadID(passenger_id)
        if is_valid_road_edge(passenger_edge):
            passenger_position = traci.person.getPosition(passenger_id)
            spatial_index.insert(passenger_id, (*passenger_position, *passenger_position))

# Function to get nearby passengers using the spatial index
def get_nearby_passengers(vehicle_id):
    vehicle_position = traci.vehicle.getPosition(vehicle_id)
    x, y = vehicle_position
    # Define a bounding box around the vehicle for spatial query
    bbox = (x - 100, y - 100, x + 100, y + 100)  # Adjust the bounding box size as needed
    nearby_passengers = []
    for passenger_id in spatial_index.intersection(bbox):
        nearby_passengers.append(passenger_id)
# Function to check if there are passengers on the current edge
def get_passengers_on_edge(vehicle_edge):
    passenger_ids = []
    for passenger_id in traci.person.getIDList():
        passenger_edge = traci.person.getRoadID(passenger_id)
        if vehicle_edge == passenger_edge and is_valid_road_edge(passenger_edge):
            passenger_ids.append(passenger_id)
    return passenger_ids
    
    return nearby_passengers
# Function to sample the observed state for a given hidden state
def sample_observed_state(hidden_state, model):
    # Get the emission probabilities for the current hidden state
    emission_probs = model.emissionprob_[hidden_state]
    
    # Sample the observed state based on the emission probabilities
    observed_state = np.random.choice(len(emission_probs), p=emission_probs)
    
    return observed_state

def predict_next_state_with_observation(nearby_passengers):
    # Manually set the state to "Passenger" or "Stoplight" if conditions are met

    if nearby_passengers:
        return hidden_state_map['Passenger']  # Set to Passenger state if passengers are nearby
    # elif stoplight_present:
    #     return hidden_state_map['Stoplight']  # Set to Stoplight state if a stoplight is detected
    else:
        return hidden_state_map['Vehicle']  # Default to Vehicle (Go) state




# Global counter for passenger IDs
passenger_counter = 0

# Dictionary to track which jeepneys are assigned stops for which passengers
jeepney_stop_assignments = {}
traditional_id_list = []
modern_id_list = []
passenger_destinations = {}

# Parse the XML file
filename = "person_flows.rou.xml"
tree = ET.parse(filename)
root = tree.getroot()



# Populate passenger_destinations from the XML file
for person_elem in root.findall('person'):
    person_id = person_elem.get('id')
    ride_elem = person_elem.find('ride')
    if ride_elem is not None:
        to_edge = ride_elem.get('to')
        passenger_destinations[person_id] = to_edge

for person_elem in root.findall('personFlow'):
    pflow_id = person_elem.get('id')
    ride_elem = person_elem.find('ride')
    for i in range(0, int(person_elem.get('number'))):
        to_edge = ride_elem.get('to')
        passenger_destinations[f'{pflow_id}.{i}'] = to_edge

print(passenger_destinations)

# Check if an edge ID is a valid road segment (not a cluster or special identifier)
def is_valid_road_edge(edge_id):
    return edge_id and not edge_id.startswith(':')

midtrip_edge = '615456195'
endtrip_edge = '16174062#0'
nearby_passengers = []
# Main simulation loop
def simulate():
    try:
        print("Starting simulation.")
        step = 0
        print(traditional_id_list)
        print(modern_id_list)
        # Initialize the state for each jeepney
        jeepney_states = {jeepney_id: {'hidden_state': hidden_state_map['Vehicle'], 'observed_state': observed_state_map['Go']} for jeepney_id in traditional_id_list + modern_id_list}
        
        while step >= 0:  # Set a reasonable number of simulation steps
            traci.simulationStep()
            if step % 1 < 0.1:
                co2_emissions = {}
                
                # Retrieve CO2 emissions for traditional jeepneys
                for jeepney_id in traditional_id_list:
                    co2_emissions[jeepney_id] = traci.vehicle.getCO2Emission(jeepney_id)
                
                # Retrieve CO2 emissions for modern jeepneys
                for jeepney_id in modern_id_list:
                    co2_emissions[jeepney_id] = traci.vehicle.getCO2Emission(jeepney_id)
                
                # Process or save CO2 emissions data as needed
                with open('Emission Output/emissions.txt', 'a') as f:
                    f.write(f"Step {step}:\n")
                    for vehicle_id, co2 in co2_emissions.items():
                        if(co2 > 0):
                            f.write(f"  Vehicle {vehicle_id}: CO2 emissions = {co2} g\n")
            if int(step) % 2 == 0:
                # Check for jeepneys and passengers on the same edge
                for jeepney_id in traditional_id_list + modern_id_list:
                    jeepney_edge = traci.vehicle.getRoadID(jeepney_id)
                   
                    if int(step)  % 1 == 0:
                        #nearby_passengers = get_nearby_passengers(jeepney_id)
                        # Get passengers on the same edge as the jeepney
                        passengers_on_edge = get_passengers_on_edge(jeepney_edge)

                    if jeepney_edge == "-29377703#1":
                      
                        traci.vehicle.setBusStop(jeepney_id, "1069829005#2", duration=30)
                    elif jeepney_edge == "16174062#2":
                        traci.vehicle.setBusStop(jeepney_id, "16174062#4", duration=30)
                    if not is_valid_road_edge(jeepney_edge):
                        continue


                    if jeepney_edge == midtrip_edge:
                        if jeepney_id.startswith("jeepney_"):
                            traci.vehicle.setMaxSpeed(jeepney_id, 12.5)
                        else:
                            traci.vehicle.setMaxSpeed(jeepney_id, 13.8)
                    elif jeepney_edge == endtrip_edge:
                        if jeepney_id.startswith("jeepney_"):
                            traci.vehicle.setMaxSpeed(jeepney_id, 7)
                        else:
                            traci.vehicle.setMaxSpeed(jeepney_id, 9)
                    else:
                        if jeepney_id.startswith("jeepney_"):
                            traci.vehicle.setMaxSpeed(jeepney_id, 7)
                        else:
                            traci.vehicle.setMaxSpeed(jeepney_id, 9)

                    current_lane = traci.vehicle.getLaneIndex(jeepney_id)
                    num_lanes = traci.edge.getLaneNumber(jeepney_edge)
                    jeepney_capacity = traci.vehicle.getPersonCapacity(jeepney_id)
                    jeepney_passengers = traci.vehicle.getPersonNumber(jeepney_id)

                    current_state = jeepney_states[jeepney_id]['hidden_state']
                    current_obs = np.array([jeepney_states[jeepney_id]['observed_state'], jeepney_passengers])
                 
                    model = trad_model if jeepney_id in traditional_id_list else modern_model
                    
                    next_hidden_state = hidden_state_map['Vehicle']

                    # Sample the observed state for the next hidden state
                    next_observed_state = sample_observed_state(next_hidden_state, model)
                    

                    # Update the jeepney's state
                    jeepney_states[jeepney_id] = {'hidden_state': next_hidden_state, 'observed_state': next_observed_state}

                    # Execute actions based on the next observed state
                    observed_state_name = reverse_observed_state_map[next_observed_state]
                    hidden_state_name = reverse_hidden_state_map[next_hidden_state]
                    #print(f'{jeepney_id}: {observed_state_name} : {hidden_state_name}')
                    if observed_state_name == 'Go':
                        traci.vehicle.setSpeed(jeepney_id, traci.vehicle.getAllowedSpeed(jeepney_id))
                    elif observed_state_name in ['Stop', 'Load', 'Unload', 'Wait']:
                        
                        if int(step) % 100 == 0:
                            try:
                                traci.vehicle.setBusStop(jeepney_id, jeepney_edge, duration=5)
                                #print(f"Jeepney {jeepney_id} set to wait at bus stop {jeepney_edge}")
                            except traci.exceptions.TraCIException as e:
                                        print(f"Error setting bus stop for jeepney {jeepney_id} at {jeepney_edge}: {e}")

                   
                    elif observed_state_name == '1 Lane Right':
                       
                        
                        if current_lane - 1 > 0:
                       
                            traci.vehicle.changeLaneRelative(jeepney_id, -1, 10.0)
                    elif observed_state_name == '1 Lane Left':
                     
                       
                        if current_lane + 1 < num_lanes - 1:
                          
                            traci.vehicle.changeLaneRelative(jeepney_id, 1, 10.0)
                    elif observed_state_name == '2 Lane Right':
                        
                        if current_lane - 1 > 1:
                       
                            traci.vehicle.changeLaneRelative(jeepney_id, -2, 10.0)
                    elif observed_state_name == '2 Lane Left' and step % 20 == 0:
                        
                        if current_lane + 1 < num_lanes - 2:
                      
                            traci.vehicle.changeLaneRelative(jeepney_id, 2, 10.0)

                    # Check if the jeepney can pick up passengers
                    if jeepney_passengers < jeepney_capacity:  # Check if jeepney is not full
                        for passenger_id in passengers_on_edge:
                            #print(passenger_id)
                            if passenger_id not in traci.person.getIDList():
                                print(f"Passenger {passenger_id} has already been removed or is not found.")
                                continue
                            passenger_edge = traci.person.getRoadID(passenger_id)
                            if not is_valid_road_edge(passenger_edge):
                                continue

                            if jeepney_edge == passenger_edge:
                                if jeepney_id not in jeepney_stop_assignments:
                                    jeepney_stop_assignments[jeepney_id] = []

                                if passenger_id not in jeepney_stop_assignments[jeepney_id]:
                           
                                    try:
                                       
                                        traci.vehicle.setBusStop(jeepney_id, jeepney_edge, duration=10)
                                        jeepney_states[jeepney_id] =  {'hidden_state': hidden_state_map['Passenger'], 'observed_state': observed_state_map['Load']} 
                                        jeepney_stop_assignments[jeepney_id].append(passenger_id)
                                        print(f"Jeepney {jeepney_id} set to stop at bus stop {jeepney_edge} for passenger {passenger_id}.")
                                    except traci.exceptions.TraCIException as e:
                                        print(f"Error setting bus stop for jeepney {jeepney_id} at {jeepney_edge}: {e}")
            # Check for passengers reaching their destination
            for passenger_id in list(traci.person.getIDList()):
                current_edge = traci.vehicle.getRoadID(jeepney_id)
                if not is_valid_road_edge(current_edge):
                    continue

                if current_edge == passenger_destinations.get(passenger_id):
                    assigned_jeepney = None

                    # Find the jeepney assigned to this passenger
                    for jeepney_id, assigned_passengers in jeepney_stop_assignments.items():
                        if passenger_id in assigned_passengers:
                            assigned_jeepney = jeepney_id
                            break

                    if assigned_jeepney:
                        try:
                            # Remove the passenger from the jeepney's assignment
                            jeepney_stop_assignments[assigned_jeepney].remove(passenger_id)
                            if not jeepney_stop_assignments[assigned_jeepney]:
                                del jeepney_stop_assignments[assigned_jeepney]

                            # Set the bus stop and unload the passenger
                            traci.vehicle.setBusStop(assigned_jeepney, current_edge, duration=10)
                            print(f"Jeepney {assigned_jeepney} stopped at {current_edge} for passenger {passenger_id}.")
                            
                            # Check if the passenger still exists before removing
                            if passenger_id in traci.person.getIDList():
                                #traci.person.remove(passenger_id)
                                print(f"Passenger {passenger_id} has reached their destination and has been removed.")
                            else:
                                print(f"Passenger {passenger_id} has already been removed or is not found.")
                            
                            jeepney_states[assigned_jeepney] = {'hidden_state': hidden_state_map['Passenger'], 'observed_state': observed_state_map['Unload']}

                        except traci.exceptions.TraCIException as e:
                            print(f"passenger already removed {passenger_id}: {e}")
                        except ValueError as e:
                            print(f"Error removing passenger from jeepney's assignment: {e}")
                    

                    

            step += 1
        print("Simulation ended.")
    except traci.exceptions.TraCIException as e:
        print(f"Error in simulation loop: {e}")
    finally:
        traci.close()

# Run the simulation

print("[1] 7AM - 9AM\n[2] 11AM - 1PM\n[3] 4PM - 6PM")
mode = int(input("Mode: "))
configFile = ""
trad_count = int(input("Enter the number of traditional jeepneys: "))
modern_count = int(input("Enter the number of modern jeepneys: "))

# Generate the XML file with user inputs
generate_routes_xml(trad_count, modern_count)
modify_person_xml(filename, trad_count, modern_count)
# Validate input range
if mode in [1, 2, 3]:
    # Assign configFile based on mode
    if mode == 1:
        configFile = "config1.sumo.cfg"
    elif mode == 2:
        configFile = "config2.sumo.cfg"
    elif mode == 3:
        configFile = "config3.sumo.cfg"
    
    # Start SUMO and connect to TraCI (assuming your existing setup)
    sumoBinary = "sumo-gui"
    # Proceed with SUMO initialization and other operations
    
    print(f"Selected mode {mode}. Using configuration file: {configFile}")
else:
    print("Invalid mode selection. Please choose between 1, 2, or 3.")

sumoCmd = [sumoBinary, "-c", configFile]
traci.start(sumoCmd)
simulate()
