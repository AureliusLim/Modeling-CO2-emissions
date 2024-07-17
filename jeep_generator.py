from jinja2 import Template

template = Template('''<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">
  
    
    <!-- Routes --><route id="r_1" edges="29377703#0 29377703#1 29377703#2 29377703#3 29377703#4 303412427#0 303412427#1 303412427#2 303412427#3 303412427#4 303412427#5 303412427#6 303412427#7 303412427#8 303412427#9 303412427#10 303412427#11 303412427#12 303412427#13 303412427#14 303412427#15 303412427#16 303412427#17 303412427#18 303412427#19 924607338 924607337#0 924607337#1 924607337#2 924607337#3 924607337#4 615456195 615456193#0 615456193#1 615456193#2 615478345 615478344#0 615478344#1 368461882#0 368461882#1 368461882#2 694268908 923261416 694268909#0 694268909#1 1176045778 82694445#0 82694445#1 82694445#2 1176045777 82694458#0 82694458#1 575729552#0 575729552#1 4086429 4332731 745183365#0 -575729108#4 -575729108#3 -575729108#2 -575729108#1 -575729555 -940627086 -4332734#7 -4332734#6 -4332734#5 -4332734#4 -4332734#3 -4332734#2 -4332734#1 -4332734#0 -4478182 -48630242#3 -48630242#2 -48630242#1 4243614#1 685156794#0 685156794#1 706706674#0 820063579#0 820063579#1 107396681#0 107396681#4 107396681#5 107396681#6 107396681#7 1148489399#0 1148489399#1 1148489399#2 1018627463 -1076442002 -4588647#5 -4588647#4 -4588647#3 -4588647#0 -917450542 1174874706 1182394700 136822582 1174874705 161754856 917450546#0 917450546#2 4637649 1158575268 1156612124 161754854#0 161754854#1 161754854#2 136822571#1 136822571#2 136822571#3 136822574 136822584 369686026 121188635 332624272 126342419 757990549 1074607189#0 1074607189#1 119883577#1 119883577#4 119883577#5 119883577#6 119883577#7 119883577#8 119883577#9 119883577#10 5019952#0 5019952#1 5019952#2 5019952#4 5019952#5 825090426 704746733#0 -187486758#5 -187486758#1 -187486758#0 16174062#0 16174062#1 16174062#2 16174062#3 16174062#4 16174062#5 176435849 820063585 -178615165 820063587#0 820063587#1 176435850 176435844#0 176435844#1 176435844#3 176435844#4 176435844#5 176435844#6 176435844#7 820063588 820063582#0 820063582#1 945948203 54338767#0 54338767#1 54338767#2 1072039865#1 704746731#0 704746731#2 704746731#3 1171640558 20816626#0 20816626#1 310627474#0 310627474#1 310627474#2 310627474#3 310627474#4 310627474#7 1074607188 940612553 757990561 121188638 126342421 136822570 757990562 136822575 136822580#0 136822580#1 136822580#2 136822580#3 295073752#0 136822587#0 136822587#1 136822587#2 136822587#3 161754855#0 161754855#1 917450547#0 917450547#2 402897988#1 32981461 917450545 1112806233-AddedOnRampEdge 1112806233 4588647#0 4588647#3 4588647#4 4588647#5 1076442002 1018627464 4258656#0 4258656#1 4258656#2 4258656#4 729164042#1 805198994#0 805198994#1 329609972#0 329609972#1 729164041#0 729164041#1 820063578#0 820063578#1 48630242#1 48630242#2 48630242#3 4478182 4332734#0 4332734#1 4332734#2 4332734#3 4332734#4 4332734#5 4332734#6 4332734#7 940627086 575729555 575729108#1 575729108#2 575729108#3 575729108#4 745183363 745183362 745183364#0 745183364#1 745183364#2 -82694458#1 -82694458#0 -1176045777 -82694445#2 -82694445#1 -82694445#0 -1176045778 -694268909#1 -694268909#0 -923261416 -694268908 -368461882#2 -368461882#1 -368461882#0 -615478344#1 -615478344#0 -615478345 -615456193#2 -615456193#1 -615456193#0 154644778#0 154644778#1 -924607337#4 -924607337#3 -924607337#2 -924607337#1 -924607337#0 -924607338 -303412427#19 -303412427#18 -303412427#17 -303412427#16 -303412427#15 -303412427#14 -303412427#13 -303412427#12 -303412427#11 -303412427#10 -303412427#9 -303412427#8 -303412427#7 -303412427#6 -303412427#5 -303412427#4 -303412427#3 -303412427#2 -303412427#1 -303412427#0 -29377703#4 -29377703#3 -29377703#2 -29377703#1 -29377703#0 29377703#0"/>
    
    <!-- Vehicles, persons and containers (sorted by depart) -->
    
   
    {% for i in range(1, 6) %}
        <vehicle id="jeepney_{{ i }}" type="traditional_jeepney" route="r_1" depart="0">

        </vehicle>
                    
        <vehicle id="modernjeepney_{{ i }}" type="modern_jeepney" route="r_1" depart="0">

        </vehicle>
    {% endfor %}
                
                    

                    
</routes>    ''')

# Render the template
output = template.render()

# Write the output to an XML file
with open('jeepney_routes.rou.xml', 'w') as file:
    file.write(output)

print("jeepney_routes.xml file has been generated successfully.")

