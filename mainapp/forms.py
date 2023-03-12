from django import forms
from django.forms import ModelForm, TextInput, Textarea
from mainapp.models import InventoryItem, Variant
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper




cj_categories = [
    ("1126E280-CB7D-418A-90AB-7118E2D97CCC", "Computer & Office"),
    ("188CE695-A4AF-48A4-B855-6BE1C7F0A44F", "Office Electronics"),
    ("2252588B-72E3-4397-8C92-7D9967161084", "Office & School Supplies"),
    ("874B7C94-D225-43FE-AB79-FFAF1B800651", "Printer Supplies"),
    ("C7365895-913A-4078-9946-681EFD45D2B8", "3D Printers"),
    ("D8BBE038-9ECD-4698-8CB1-DE63E27F33C7", "3D Pens"),
    ("E33443F7-144C-4CBE-8D34-C1B6256A6325", "Printers"),
    ("F8024D10-AB96-4558-AC79-C49625F768DA", "Scanners"),
    ("192C9D30-5FEA-4B67-B251-AF6E97678DFF", "Security & Protection"),
    ("0598E853-9BF7-4939-A571-2407E819C91E", "Alarm & Sensor"),
    ("0ACCE01C-2C83-4767-B9E8-736B7E0CC38D", "Fire Protection"),
    ("0B50EC4B-F78C-4D2D-839C-4767D6B4B7C7", "Workplace Safety Supplies"),
    ("28F0E5A1-0A9A-43C5-8197-F1420A9BD10B", "Door Intercom"),
    ("BB57B72C-A8C6-40FF-BCBB-EAE0251273C6", "Surveillance Products"),
    ("23AD5346-5552-4392-A922-69CE426EC583", "Storage Devices"),
    ("4D3B9582-E92E-46BF-B00E-715E70FB4742", "SSD"),
    ("591E8920-019B-42FA-AE0B-420052E6C4F0", "USB Flash Drives"),
    ("76B88FB8-9B37-4B55-AA09-082C5627DFE8", "HDD Enclosures"),
    ("7E65A403-CF6E-4B55-96FF-B7C3C376A47A", "Memory Cards"),
    ("C62BC6BF-BA2B-41ED-AB12-599A6D7FCAA5", "External Hard Drives"),
    ("764DB83F-C286-4CA9-9ACF-4017CFC86A39", "Tablet & Laptop Accessories"),
    ("24FAA1AB-BF10-41ED-8405-A9FA53031B3A", "Tablet LCD Screens"),
    ("3F3EFC96-82B8-44C1-BF7A-2E3E7083A875", "Laptop Batteries"),
    ("74B144C9-321D-4E78-986C-757BA551DD8C", "Laptop Bags & Cases"),
    ("87A618B5-7CB0-4AF7-BCF8-9E9455F06B7E", "Tablet Cases"),
    ("EDC3EDAF-1ED7-4776-8416-E9F8F0A5B4C6", "Tablet Accessories"),
    ("7ECEEABC-0396-411D-969A-8F69CC7369E5", "Laptop & Tablets"),
    ("1E9A3E86-7E5A-439E-9B33-CBD495421F0B", "Phone Call Tablets"),
    ("25E64DFD-1ED3-4171-86CD-0C2F40052F3B", "2 in 1 Tablets"),
    ("7D962F30-E20E-4DE9-8911-EB8AB078FB23", "Laptops"),
    ("D190FBF9-A352-48BD-9F4B-B6AB432988E5", "Tablets"),
    ("E3963C40-89BE-46AC-985D-A86FA417F6B8", "Gaming Laptops"),
    ("E79489E4-8022-42F5-9847-9B4543C8763F", "Networking"),
    ("4F7EE88B-4209-42E8-A501-5F634B58BB35", "Modem-Router Combos"),
    ("76CD1BD4-2A0A-4D72-913C-6DAADD7E9EDB", "Wireless Routers"),
    ("9A33970D-F4BC-48EC-BEAB-FEC19C130963", "Networking Tools"),
    ("A77A4E59-D931-4BBE-9D48-FF995C481B66", "3G Modems"),
    ("C019C59C-C274-44F9-B04B-5520F1EBE5FA", "Network Cards"),
    ("2415A90C-5D7B-4CC7-BA8C-C0949F9FF5D8", "Bags & Shoes"),
    ("D82A6AF3-78F1-4A33-8F44-A37F282B2209", "Men's Luggage & Bags"),
    ("9F5FDE97-3BE8-4EBE-A8EA-48723A307E37", "Briefcases"),
    ("B701FAC3-80F0-43B1-9EA5-2C05C55F582A", "Waist Bags"),
    ("C50C5B6E-1517-4CBE-97FE-ECC923C83D35", "Girls Bags"),
    ("CDCCB9B1-D5DD-4C20-AF32-101FE427B63C", "Men's Backpacks"),
    ("E89AC661-0B9E-4967-A0A3-7B0C6DEDDC7D", "Luggage & Travel Bags"),
    ("EA292A58-E696-428B-8BEB-DE105690DDB3", "Crossbody Bags"),
    ("F3F4B418-17DF-49A1-AD76-A436B7618FFC", "Man Wallets"),
    ("E93B19EF-4E2C-4526-B2DF-BBFB6F2A80A7", "Women's Shoes"),
    ("1988B912-7A18-4ED2-B1E1-61ED290A0E82", "Woman Boots"),
    ("1B559D30-B370-4C8E-8CFD-1E1BC47E217F", "Vulcanize Shoes"),
    ("638284D0-3651-4FC9-9F25-B0A0BA323D83", "Pumps"),
    ("8F756420-4840-474E-B2D6-6725ED219970", "Woman Slippers"),
    ("AAB54987-4E92-40C7-B0F5-5E814C1E6980", "Woman Sandals"),
    ("F35FC838-1CFE-49D1-A8CA-CF7401F9C444", "Flats"),
    ("EC2E9303-E704-43F3-834A-A15EA653232E", "Women's Luggage & Bags"),
    ("0ADE366E-CDF4-47E7-8720-B480220E1BD4", "Woman Wallets"),
    ("33AFFE07-CC46-4557-9FD9-27CC9975BEED", "Evening Bags"),
    ("78BCE010-8E22-416F-82E2-6E5C6AE0CECE", "Fashion Backpacks"),
    ("7DC7FA45-C8E1-4A2E-BA84-B81FB9CA2815", "Shoulder Bags"),
    ("8F3ADC01-68FE-4CBE-BB1D-0DE42A730749", "Totes"),
    ("96C833A9-93EC-4D76-B093-3A3B945659C6", "Boys Bags"),
    ("CB7C7348-41DC-4AA5-9BD0-CC2D555899BB", "Clutches"),
    ("FE8AD446-B2BF-4C8C-B90B-49A6F2B3FF6A", "Men's Shoes"),
    ("0F0296D6-F057-4FD4-9E06-95D5DBCCE6EB", "Man Boots"),
    ("11C9DE73-0438-40E2-80B8-72697795C9F2", "Formal Shoes"),
    ("312428E8-5075-4F74-A317-8EB051C0C068", "Man Slippers"),
    ("B8640E7B-F07D-4C0F-A5CF-8ACC533DA86F", "Vulcanize Shoe"),
    ("D0E37ED0-65C8-43E3-8B84-C973040DCE9C", "Man Sandals"),
    ("F419006D-AE55-4691-93FC-52FEBB459DBA", "Casual Shoes"),
    ("2837816E-2FEA-4455-845C-6F40C6D70D1E", "Jewelry & Watches"),
    ("01114D8D-79BD-4AD9-85A0-72D1B050E3F8", "Wedding & Engagement"),
    ("04B879BE-79E7-4CB9-B493-B03F628B5130", "Bridal Jewelry Sets"),
    ("443467E0-29C5-4850-9BF4-B0D8F9008EEB", "Wedding Hair Jewelry"),
    ("FCE034F6-A2BF-47E3-852F-FA9F67F904B2", "Engagement Rings"),
    ("FCF87613-7AF4-4053-B688-B415FDD242CE", "Wedding & Engagement"),
    ("123ACC01-7A11-4FB9-A532-338C0E7C04C5", "Fashion Jewelry"),
    ("0615F8DB-C10F-4BEF-892B-1C5B04268938", "Bracelets & Bangles"),
    ("1363024200339689472", "Brooches"),
    ("1363289906151034880", "Keychains"),
    ("2909669F-96C4-457A-A425-19799F2A47BF", "Charms"),
    ("56B4F8B6-8600-4A18-913E-53F2F693EC2C", "Rings"),
    ("633E1860-7C63-4006-AB35-3FC16BECFA62", "Body Jewelry"),
    ("89D165E3-EF5F-461D-9DC9-D1041CECEF09", "Fashion Jewelry Sets"),
    ("95D9F317-1DB3-4E42-A031-02223215B9C5", "Necklace & Pendants"),
    ("B5525066-3504-4E5C-962F-9C2D8C38F66D", "Men's Cuff Links"),
    ("D28405AE-66C6-42E6-BFF0-D6FDCB5C083C", "Earrings"),
    ("3E53507E-2EDB-49F1-8D0D-AD01225DAD8A", "Fine Jewelry"),
    ("391F1C45-D86B-4A92-893E-48C1CA84C461", "Various Gemstones"),
    ("552F095A-904C-40E4-A43B-0CD1CE15D29F", "925 Silver Jewelry"),
    ("7BCF191E-A4CC-403E-AF46-81370EB3AB19", "K-Gold"),
    ("84ED4B7F-D7C3-412F-AF18-04F25C91985C", "Pearls Jewelry"),
    ("D7CE9827-F50A-4B07-84BF-1BFE44188A1C", "Fine Earrings"),
    ("E403FB8A-B59A-4A81-B776-EBF3343FE3E3", "Men's Fine Jewelry"),
    ("E8B256EF-44F0-4FA0-847B-F104FD29E101", "Fine Jewelry Sets"),
    ("603B4E08-4226-4BFC-A46E-FCCE92ED1C63", "Men's Watches"),
    ("1987B0AD-8C6A-4D02-B5B2-5D94E83B069F", "Quartz Watches"),
    ("369EB061-A5CD-4F1F-A105-6DAB1D520F49", "Mechanical Watches"),
    ("3D882765-B20E-4EFD-BFCC-136942A83C4C", "Digital Watches"),
    ("76B0FCF7-2571-4B64-AE23-82D6A15C4C19", "Dual Display Watches"),
    ("BF68CA3E-F698-475E-A1AD-C8E4C44D7C8D", "Men Sports Watches"),
    ("F1B0B876-9103-4DF0-9EA5-524094648BFD", "Women's Watches"),
    ("9D78B3E3-99F4-4EDA-8C70-2F5B95061CAA", "Women Sports Watches"),
    ("A044AC0D-BA3B-4967-8300-1BD57F00048E", "Dress Watches"),
    ("DAE17D16-A15F-445D-AE34-B698F3290E56", "Creative Watches"),
    ("DC682F4C-BD7E-4DB0-93CB-33B4CD54BE87", "Lovers' Watches"),
    ("F40CB152-1391-4CA9-9BAE-0316DA2D3D2B", "Women's Bracelet Watches"),
    ("FBD85934-5409-4EC6-A6B5-FDBF072AA0E2", "Children's Watches"),
    ("2C7D4A0B-1AB2-41EC-8F9E-13DC31B1C902", "Health, Beauty & Hair"),
    ("01FD30A0-118E-4269-A6D2-8415E9C163BA", "Nail Art & Tools"),
    ("1B1A9B82-1833-4721-88CA-86F5F542D7A5", "Nail Glitters"),
    ("25A6516D-3AE3-4207-BA00-6FD3CCE20201", "Stickers & Decals"),
    ("26F7660F-A00A-468A-BA29-E61A465C0D0B", "Nail Decorations"),
    ("9F96CE84-962D-4992-81DC-BF79A4A9002D", "Nail Gel"),
    ("E157D35B-156B-49F6-A678-7C55D4E81D6C", "Nail Dryers"),
    ("EADB666A-12A5-4FA1-AD1F-BC351A7E7AF5", "Nail Art Kits"),
    ("3B5BDD4D-34F4-4807-BC6C-943C2C1BCDB8", "Hair & Accessories"),
    ("B3D7C9CA-9B1E-4E97-8310-39083F0308C9", "Human Hair"),
    ("3C677D1C-C1AA-461F-851F-3E8A42C82984", "Synthetic Hair"),
    ("C8148B69-25D4-4DEE-8388-3D627D35163D", "Cosplay Wigs"),
    ("6289460B-5660-468A-AE43-3D619A05AAC2", "Skin Care"),
    ("5DE3BC4F-41A8-4806-8E66-47537903123A", "Razor"),
    ("88AF62DE-5586-40E4-A287-864523D9AE50", "Face Masks"),
    ("B6A8B971-793B-4F9E-AA56-3A5D12F63827", "Sun Care"),
    ("CB1A9CEF-8333-4D2F-B19A-418C6DE376C7", "Essential Oil"),
    ("E0238E88-0C63-427F-812E-BA1FCE4C67B4", "Body Care"),
    ("EDE3FAD9-0E6C-4F7C-9016-A2299469AA7C", "Facial Care"),
    ("71BB975B-A54E-489E-95BF-3105433858D0", "Hair Weaves"),
    ("4B3ED595-B44D-4A7A-81F8-B0E3B272B62A", "Pre-Colored One Pack"),
    ("57DCC498-DF74-4E8F-929F-F4DF256AA72D", "Hair Weaving"),
    ("9A3105F2-AFFD-42FC-8A52-D0FB4ACDCB63", "Hair Styling"),
    ("C6368BAF-38E8-4741-86F3-66878F069841", "Salon Bundle Hair"),
    ("D7EF49F5-F75D-45DC-A0BB-CFCFF4346E18", "Pre-Colored Hair Weave"),
    ("7EAF3E36-620B-4D78-818F-EE80955462A4", "Makeup"),
    ("426792A7-4906-403D-AD17-8293AFF00E66", "Makeup Set"),
    ("8FB2C16C-4C1B-4B5A-89F8-BC30FB2C442A", "Eyeshadow"),
    ("A30E8F55-DC2C-4842-9372-91B96DEFDCC2", "Makeup Brushes"),
    ("B68DF53F-4DD5-4659-A530-66D414CF2147", "Lipstick"),
    ("E31E5996-7B86-4FEC-B929-9AEB11E76853", "False Eyelashes"),
    ("BF7AE6E9-E175-48FD-B1E3-3CF0126C90D0", "Wigs & Extensions"),
    ("44733589-BEE4-448D-86F9-A1B5A9710C79", "Human Hair Wigs"),
    ("6ADDD8E4-4141-4B5A-9A85-6D87FED7799C", "Synthetic Hair Pieces"),
    ("6C4CEB64-10FD-447E-BB1D-F6F5C1E71442", "Synthetic Lace Wigs"),
    ("93B5702F-DEF0-443D-847B-9287DEDF5BD9", "Human Hair Lace Wigs"),
    ("B30591BD-0353-4791-8BF6-F4876CC7F9B1", "Hair Braids"),
    ("DB81767B-2083-4C66-8E8D-1A0D897ABA7C", "Synthetic Wigs"),
    ("CE5FADBB-B432-40B9-8B20-200F6928762A", "Beauty Tools"),
    ("47D355FB-E6C1-4E0B-AE31-0B1696A4B68E", "Straightening Irons"),
    ("6D086E0D-8C3F-4B99-BA44-140F3F7C444E", "Electric Face Cleanser"),
    ("8E00C4BE-1E35-43E7-A891-6CAE58BB48CF", "Massage & Relaxation"),
    ("AB11F624-D292-4A8E-9284-BD368B893A2C", "Face Skin Care Tools"),
    ("C75F27EE-695C-423E-BCB4-7CFE67221332", "Curling Iron"),
    ("D23FFB85-4185-4FA3-BAF0-224A4F516741", "Facial Steamer"),
    ("2FE8A083-5E7B-4179-896D-561EA116F730", "Women's Clothing"),
    ("23DDAF61-8F6C-40F7-9F1F-DC9BB25450B6", "Accessories"),
    ("0DC4DF6F-4EC5-47DF-B20D-863ADF69319F", "Scarves & Wraps"),
    ("1374953557614268416", "Face Masks"),
    ("1E4A1FD7-738C-4AEF-9793-BDE062158BD6", "Belts & Cummerbunds"),
    ("2EB0613C-E73D-4A09-A21C-90E5F1C227D3", "Woman Prescription Glasses"),
    ("3B4C41C0-EA46-4F03-A2F4-9A9948947439", "Eyewear & Accessories"),
    ("7B2039D9-FF87-4514-954B-021289724271", "Woman Gloves & Mittens"),
    ("96EBD53A-C941-445C-BBBD-C1D9F858E433", "Woman Socks"),
    ("F72DD534-E394-4958-B591-149C488648D7", "Woman Hats & Caps"),
    ("422D4713-284A-49EE-8E53-680B7DCC72FE", "Tops & Sets"),
    ("1357251872037146624", "Ladies Short Sleeve"),
    ("5A3E7341-18B5-4C61-BFCD-8965B3479A9A", "Blouses & Shirts"),
    ("5E656DFB-9BAE-44DD-A755-40AFA2E0E686", "Woman Hoodies & Sweatshirts"),
    ("67E91AA2-83EE-44B5-A308-DEC0643FF53F", "Intimates"),
    ("7B69E34F-43A3-4143-A22D-30786EE97998", "Jumpsuits"),
    ("7D611AF5-5135-4BBB-86F6-E80179F8E5B8", "Rompers"),
    ("8B95183C-E835-4B9D-97DB-E7708F1A89B9", "Sleep & Lounge"),
    ("D2432903-0D4E-4787-886F-D3D9DA7890D9", "Lady Dresses"),
    ("DE9C662C-3F48-4855-87E7-E18733EFF6D2", "Sweaters"),
    ("ECDBD4C4-7467-4831-9F55-740E3C7968BE", "Suits & Sets"),
    ("4257920C-6E7D-4B56-B031-0FC7AC6EF981", "Bottoms"),
    ("396E962A-5632-49C2-B9BF-9529DE3B9141", "Leggings"),
    ("3B8946E7-B608-4DAB-B2F0-C425B7875035", "Skirts"),
    ("63584B9B-5275-4268-8BEA-7D3C7A7BB925", "Woman Jeans"),
    ("8A22518D-0C6F-430D-8CD9-7E043062A279", "Woman Shorts"),
    ("9694B484-7EA0-4D71-993B-9CF02D24B271", "Pants & Capris"),
    ("A7DE167B-ECFF-481E-A52A-2E7937BFAA95", "Wide Leg Pants"),
    ("6D2A8F6D-4AF4-421D-840D-B5C1E52C3A75", "Underwears"),
    ("A6158EC0-C66D-456D-923C-E784EE432A02", "Bras"),
    ("CA7192AE-4B6A-40F6-9FB8-C7152AAA3001", "Panties"),
    ("773E0DBE-EEB6-40E9-984F-4ACFB0F58C9A", "Outerwear & Jackets"),
    ("07398ADB-FC5E-4CC4-AD00-EB230E779E88", "Blazers"),
    ("1366AF62-E9CB-4834-9EC9-6126C077B5E0", "Wool & Blend"),
    ("441DA450-5E5F-41DF-8911-3BAE883C30E8", "Woman Trench"),
    ("4CF7E664-A644-4B96-951B-B76FA973320A", "Basic Jacket"),
    ("D680731F-1AE8-46E4-9BE7-E98C39F07E1E", "Leather & Suede"),
    ("F5C6B4C3-0362-40D3-811B-19C37C5C4AC2", "Real Fur"),
    ("85CC5FF8-1CAC-4725-9F07-C778AB627E1B", "Weddings & Events"),
    ("1AFD1C87-0BB1-4BAB-AA1A-D082E767811C", "Cocktail Dresses"),
    ("30E8E5CF-FBBA-48DA-84DD-E29D733089E0", "Evening Dresses"),
    ("6C2516C4-F999-434C-B3F4-467FAFA13E2E", "Bridesmaid Dresses"),
    ("88E43313-84C6-4550-B2C7-83A415AFA2DD", "Prom Dresses"),
    ("935BCF1B-5D61-422F-8439-19179FE8B492", "Wedding Dresses"),
    ("95C53342-6277-4FEC-B450-6D3F9EEDD6A1", "Flower Girl Dresses"),
    ("4B397425-26C1-4D0E-B6D2-96B0B03689DB", "Sports & Outdoors"),
    ("1E2633D4-2F96-4E2A-ABF7-BCBF3DFEE28A", "Sneakers"),
    ("24A29AC9-8B9B-4552-AF5E-431E6CF47C67", "Running Shoes"),
    ("3928EB2C-04C4-4862-BCBD-A4987005A629", "Dance Shoes"),
    ("4B83DB4C-2D1F-4FA4-8844-FC39C6DBD60B", "Skateboarding Shoes"),
    ("5F140735-E3D7-46A0-A28D-34607B05B720", "Hiking Shoes"),
    ("9DA4624F-A8A2-4DC1-9088-81877A4944F2", "Soccer Shoes"),
    ("C8FD79F7-DF24-495F-BE12-5F8585A8E5ED", "Basketball Shoes"),
    ("36492F79-E7EB-42F0-8DCC-6129BD9D2AE1", "Other Sports Equipment"),
    ("02FB2558-F014-4E0A-A2FE-30BE514A2B01", "Musical Instruments"),
    ("2D818FE8-522E-4102-B659-F807564251ED", "Hunting"),
    ("8B8C7FFB-6686-4994-B6DB-E5B8C1AAC9A6", "Skiing & Snowboarding"),
    ("C20B25A2-348C-48C8-A2C8-FE33749A40DE", "Fitness & Bodybuilding"),
    ("EA851596-F20F-4AA5-8869-4BB5CA1968DC", "Camping & Hiking"),
    ("FD5E95E1-C8DC-4CBD-A203-8BCF3BA951B9", "Golf"),
    ("4B36F14A-6894-4047-8845-56CAFCF9A914", "Swimming"),
    ("0653C2F4-A393-4BD1-B903-7B0569960868", "One-Piece Suits"),
    ("56F1151E-2544-4044-BB41-03081A532B2F", "Bikini Sets"),
    ("5E554D7C-64F3-4457-82AA-B0483EED26FB", "Two-Piece Suits"),
    ("76C86F19-2411-450E-8F69-DDE1DC6580E9", "Men's Swimwear"),
    ("7B7C97C3-34E3-4DC6-A639-FB7FA421E146", "Cover-Ups"),
    ("9CFD57D3-3BEB-498F-85F1-C752C4937D75", "Children's Swimwear"),
    ("55A1D05D-A254-4242-A4BD-4BE88F0680B6", "Cycling"),
    ("161FA128-487C-4451-8B49-CB81B5A30A54", "Bicycle Lights"),
    ("3D0169CF-0F24-4EEA-948E-E48C3980862E", "Bicycle Helmets"),
    ("7992143D-A8B2-4A05-A4E4-7F4AF73AA577", "Cycling Eyewear"),
    ("A0A24BC7-F4F4-4090-9D83-6ECA1F4A78FD", "Bicycle Frames"),
    ("BE08AC4E-D953-413F-93FC-452F635E73EC", "Cycling Jerseys"),
    ("FF18DE9F-3D6A-48A0-A246-EF5B1D0D4E0E", "Bicycles"),
    ("66C86053-159B-436E-B4A9-4A7CCB5CAC8A", "Sportswear"),
    ("5A053E55-5D18-42EF-A4E7-B08AEA4D9B2F", "Jerseys"),
    ("79F47CD1-F813-4B4D-8D21-2B35966FBA66", "Sports Accessories"),
    ("8E8CE199-A134-45B1-9EDE-0D4F122F4568", "Outdoor Shorts"),
    ("937A06CE-ECCC-4C7D-A270-B216DE612AC0", "Sports Bags"),
    ("AB04A021-C988-476D-88E7-3CAAE3019D9E", "Hiking Jackets"),
    ("FE1DB733-120C-4506-B990-107EAC5E62E5", "Pants"),
    ("CD4184EB-CD02-4789-8CFA-8FF3B4DEFC4E", "Fishing"),
    ("11E0FCD6-AD17-4F72-B5FF-8F8C79F85CE5", "Fishing Reels"),
    ("1210D5B0-E172-47F8-8ADA-E3280624F5A5", "Rod Combos"),
    ("37C76B77-3E08-456A-B184-4516E7D6EE81", "Fishing Tackle Boxes"),
    ("9704D88F-46A0-49F6-98C4-929AE91941F5", "Fishing Lures"),
    ("B27D0790-81A0-484A-9D92-0AFBA04FDA31", "Fishing Rods"),
    ("E2019E0B-EDC1-4B90-8C65-EE6A87AF7E73", "Fishing Lines"),
    ("52FC6CA5-669B-4D0B-B1AC-415675931399", "Home, Garden & Furniture"),
    ("1AD00A3C-465A-430A-9820-F2D097FDA53A", "Home Textiles"),
    ("1A9A9965-A914-46D7-B8E2-49AD256F2B6B", "Curtains"),
    ("300CC260-CF9D-4AEA-9FC2-6C8DB8A35B51", "Cushion Covers"),
    ("331F43CE-CA1D-45F2-BE2A-8AE62EC10251", "Towels"),
    ("36F37524-3EAF-4E20-B989-10137FD0ED70", "Comforters"),
    ("496E6FFC-4BC4-4CA6-8225-5BC0D56E8E11", "Bedding Sets"),
    ("6939DA08-F7F8-48FB-A7E8-169AEAC92404", "Pillows"),
    ("2180A6DC-32EC-44B2-8FD4-CE3DD6DB4C19", "Arts, Crafts & Sewing"),
    ("664B9B04-4697-437A-AA46-631EFCC3DF03", "Lace"),
    ("93671B1A-DE8F-4398-B139-8B2214206648", "Apparel Sewing & Fabric"),
    ("C8AA2A38-B339-468F-87D3-AD2DB0697F93", "Cross-Stitch"),
    ("D60B979B-3779-47BD-8F55-D17581817273", "Ribbons"),
    ("EEC881A3-0A55-4BBF-9ADB-EB290116A67A", "Diamond Painting Cross Stitch"),
    ("FD2629CD-9379-4EC4-BCF3-5998AEA3E642", "Fabric"),
    ("7D40D0BB-1466-4EEA-B275-0EB4CC0020D8", "Festive & Party Supplies"),
    ("621F9C38-814C-40C2-9F9D-7CE12DB8FB4C", "Christmas Decoration Supplies"),
    ("768DE38B-3FCB-4DD1-B14C-687F03F78D0A", "Invitation Cards"),
    ("779524FE-7E6E-4948-A739-999E07602BE5", "Cake Decorating Supplies"),
    ("7B975B46-46DF-4C3A-BC58-1F4F2DDB9413", "Decorative Flowers & Wreaths"),
    ("9F52617D-F420-4FA7-8F25-53A9577A9111", "Party Masks"),
    ("C329460A-9074-4E42-B1FD-D9E91568A64B", "Event & Party Supplies"),
    ("CC4A7507-4A32-40CC-B053-825C73F705CA", "Pet Products"),
    ("71D5774E-3B4A-4BB0-B89B-942927D53AD8", "Dog Supplies"),
    ("84FCDDEF-179D-4D37-AA00-0E26F80EC76D", "Bird Supplies"),
    ("B9B9AD50-DBB7-4137-86EF-ABCEA5ED6D3D", "Cat Supplies"),
    ("C87A4C57-ABB5-4752-A89D-94C4E8875336", "Fish & Aquatic Pets"),
    ("E07CF784-00B2-4B1D-8806-02BE80077EF4", "Dog Clothing & Shoes"),
    ("E23EA4D5-C5F5-4290-98F8-7B685B059397", "Dog Collars, Harnesses & Leads"),
    ("D5D120D0-1262-461A-97C5-74AC732625B5", "Kitchen, Dining & Bar"),
    ("0F4CFA22-8B97-4016-94A6-18066B9BD05C", "Dinnerware"),
    ("23ADD7CB-065A-4A02-B8E8-43D3F041B90B", "Kitchen Knives & Accessories"),
    ("7C8E809A-460A-4F50-8A2F-B62AD010BFF8", "Bakeware"),
    ("BEDFD1CC-E7CC-438F-9050-D7737904203D", "Barware"),
    ("CF330457-0E5B-4FAF-9BAE-7D2C247BD8DE", "Drinkware"),
    ("E448A723-43DC-4BD8-A9AD-2FB9699338B4", "Cooking Tools"),
    ("ED8E61AA-2260-4E03-BA66-DEAE3DF02CDC", "Home Storage"),
    ("56845C3D-4D9E-4729-B5D4-6D7DE310C031", "Kitchen Storage"),
    ("87CF251F-8D11-4DE0-A154-9694D9858EB3", "Home Office Storage"),
    ("A0E89009-FFD6-4B2E-906A-8076DF45B32C", "Clothing & Wardrobe Storage"),
    ("B62EE40F-7650-4715-A7A5-BA227540593C", "Bathroom Storage"),
    ("C1394E10-1EDF-4107-AA93-F142B44C3136", "Storage Bottles & Jars"),
    ("6A5D2EB4-13BD-462E-A627-78CFED11B2A2", "Home Improvement"),
    ("392D3DB2-1E98-474E-9E45-9F2FE95A7608", "LED Lighting"),
    ("DFFFDEDF-42F8-4D1F-B0A3-6B6744F7C1D3", "LED Spotlights"),
    ("59AEBD05-0FDB-4392-BCF5-518C411A26E0", "Outdoor Lighting"),
    ("7E431502-1275-4FF3-A236-B97C107C3AFA", "Flashlights & Torches"),
    ("A33B0665-E26F-4870-B2B3-B13B4C36EE66", "Floodlights"),
    ("E6271C99-8F7B-457D-AE11-3950081DD093", "Underwater Lights"),
    ("EDB5F43E-EAC0-489A-8355-5188EAB72D08", "String Lights"),
    ("F9749558-9C47-4612-9411-88FF301DB7AD", "Solar Lamps"),
    ("67391D45-D736-40E9-9D90-F56418804ECC", "Tools"),
    ("4D7853CE-9E1C-4103-A06F-46401827A535", "Measurement & Analysis"),
    ("4E013A02-FB26-4CA4-998C-85CC07623984", "Welding & Soldering Supplies"),
    ("52500EBD-C120-4C0E-9EF8-0F381E530633", "Welding Equipment"),
    ("55795653-09E8-4EE6-B477-1E30E7A601B2", "Hand Tools"),
    ("7B18EF9A-B48E-4917-84AF-624919C32CA6", "Tool Sets"),
    ("924090C3-8179-437F-8219-37582113FB08", "Tools Storage"),
    ("964AB089-A154-4971-9A4F-DB9C57E06854", "Machine Tools & Accessories"),
    ("9FC79C6B-AE70-472C-B8F8-D62479F0D03E", "Power Tools"),
    ("C9F154F8-5782-40E7-B749-3CF89763F16D", "Woodworking Machinery"),
    ("CDB10A90-3D34-4396-99B2-919E7CAD4B53", "Garden Tools"),
    ("85EF081C-819E-448F-BD5C-C5D3F4CFAADA", "Home Appliances"),
    ("02EA33AA-4174-497D-86F4-D4FF9E525B81", "Personal Care Appliances"),
    ("3633986F-83D2-4A6F-8F4D-79EE2CF77B8F", "Cleaning Appliances"),
    ("36686698-230D-46F9-A076-8CC61AE36CE3", "Air Conditioning Appliances"),
    ("4D91D172-D6D0-429E-AABC-6F3325A273A6", "Home Appliance Parts"),
    ("A028998B-C8CF-4533-BBE4-E04FA244CDC6", "Kitchen Appliances"),
    ("BEFFF5CB-EF79-4984-9C55-62C23B95C0F7", "Indoor Lighting"),
    ("02795B1D-0E81-4201-B6D5-19A2605DEC10", "Chandeliers"),
    ("0591D043-4EFC-494A-9901-358197CC3D18", "Pendant Lights"),
    ("36C55794-4437-4782-B8CF-D265C12CA4E5", "Downlights"),
    ("538CB48E-B7A0-46F7-B5A2-BB8183247B23", "Night Lights"),
    ("AC4A8F93-27FF-4531-8394-53E97F02159D", "Wall Lamps"),
    ("D6A70719-5E93-40E6-AE8B-A060D667A17B", "Ceiling Lights"),
    ("A2F799BE-FB59-428E-A953-296AA2673FCF", "Automobiles & Motorcycles"),
    ("1D5C8310-38DC-436D-B281-37660F7673B1", "Exterior Accessories"),
    ("255A489E-8518-4E31-AC84-A2E8EB645C78", "Car Stickers"),
    ("ED1BECF0-0B39-41EE-968C-2948FED771C3", "Other Exterior Accessories"),
    ("ED8B5070-DA72-451A-A0BF-DBE65FDA465E", "Car Covers"),
    ("575086BA-B96B-4557-85C9-004D3DF6A9AE", "Interior Accessories"),
    ("090E48F4-B406-438B-9EBF-D52450AC370A", "Floor Mats"),
    ("309854A6-BDC2-4F52-80D8-93E5109B3A53", "Key Case for Car"),
    ("5559DD57-7F12-44BC-9C29-9E9BD1CDB029", "Steering Covers"),
    ("808A409E-8E16-43A8-879A-153672135DB9", "Automobiles Seat Covers"),
    ("D44C3391-0AF1-455A-A671-29214DA68F27", "Stowing Tidying"),
    ("8D23F08A-3D9E-4A29-A184-EB6F8145E739", "Tools, Maintenance & Care"),
    ("00E6FC51-B865-4D50-9EF9-21E7050F5653", "Car Washer"),
    ("3627FAE5-F4A4-4227-8066-A7D460BA6E21", "Diagnostic Tools"),
    ("77A90826-779B-47DD-AB79-8FEE91AE0A3E", "Paint Care"),
    ("D24CEB99-1ABB-4643-B0B6-33C60AF9B101", "Other Maintenance Products"),
    ("AE1E932F-7832-4CE8-9DFE-885044383863", "Car Electronics"),
    ("10B94E89-4E22-4BC8-8E6C-9A5CB2119F03", "Vehicle Camera"),
    ("2A64C22F-F04A-4AAA-9C1C-8AF89323FB63", "DVR & Dash Camera"),
    ("4B2ED078-B253-4105-98A2-1203875448F5", "Car Monitors"),
    ("5D2C4AD8-AF51-4258-A329-45A675E2805D", "Vehicle GPS"),
    ("5F6BBD36-AFDE-4433-81D1-8684781E04DE", "Car Mirror Video"),
    ("A3E67E41-8A5C-449F-8C22-739889760AAD", "Car Radios"),
    ("B39B6F95-9C89-4D6C-9E98-1633DA6A51CF", "GPS Trackers"),
    ("B43C754E-838C-4028-99E7-D3D0E029C68C", "Car Multimedia Player"),
    ("BCC009E7-B5FF-4E4B-8D1D-7DE5B5DBFAE0", "Alarm Systems & Security"),
    ("C7B399B2-4D26-4363-8062-C6F451DA55B3", "Jump Starter"),
    ("D82400A8-94A4-410C-9155-0DCD4115DEA4", "Motorcycle Accessories & Parts"),
    ("11B12208-A434-467B-8AD3-DC65E32EC2E5", "Lighting"),
    ("45EA5F91-6654-48C5-8D3A-0E5E97156F16", "Exhaust & Exhaust Systems"),
    ("482DBC73-CA1B-4FF5-A943-D282D7FBC18F", "Motor Brake System"),
    ("4FB5AA23-AA52-4928-A653-616ED3347074", "Motorcycle Seat Covers"),
    ("628E44C8-73BF-4D4C-87C9-0B4F9A60D0C3", "Other Motorcycle Accessories"),
    ("683FC820-3B12-4F92-A250-FF213D8D3899", "Helmet Headset"),
    ("9EB55782-830D-41A5-B29C-B5A13520923E", "Body & Frame"),
    ("FBA0652F-AC56-4EB6-9360-8CE42B83BF48", "Auto Replacement Parts"),
    ("28508884-954A-4F76-83BC-FAEA0E0C43FE", "Interior Parts"),
    ("3166F1D4-5213-42D7-A2B6-670ACF0D489A", "Car Brake System"),
    ("9F6B73A9-0E4F-4EE9-978F-69984CF3E300", "Spark Plugs & Ignition System"),
    ("C8B7A95E-0E98-41F8-892B-35B5679713A6", "Automobiles Sensors"),
    ("CAE924E7-EB56-4299-A5B0-8DB86C9ECB52", "Exterior Parts"),
    ("CB255FA6-9B4C-4542-82CC-F774DE8F8C68", "Other Replacement Parts"),
    ("E987126C-FF3D-4BCF-B496-40990D39D2F8", "Car Lights"),
    ("FF672D98-F632-4C18-ABA3-E86C9C8951FE", "Windscreen Wipers & Windows"),
    ("A50A92FA-BCB3-4716-9BD9-BEC629BEE735", "Toys, Kids & Babies"),
    ("04D68B68-1048-4971-BAFA-18FA0A6DB95C", "Toys & Hobbies"),
    ("6614840A-DB50-4FBB-80FD-705F4FD59BFA", "Electronic Pets"),
    ("835F7743-8432-4D0F-90F0-E76C89F7C5B7", "Blocks"),
    ("AEABDF3C-35E9-4BDA-8F5B-DA602BC5B9C8", "RC Helicopters"),
    ("DD918287-C279-466A-B9C6-56079DE4B37A", "Stuffed & Plush Animals"),
    ("F18491A9-2F33-4D85-A154-78EE4CD2AD33", "Action & Toy Figures"),
    ("0F88CF9B-C46C-491B-8933-115806ED8A13", "Shoes & Bags"),
    ("5AF1783E-547C-44E5-AD8A-82B354860BCB", "Boys Shoes"),
    ("62A4235C-31EE-40E3-9D61-8F310470FEBC", "School Bags"),
    ("929F5F58-AFBB-43AE-B1BB-CC6AA3844530", "Kids Wallets"),
    ("C6FBABFE-2E34-4BD8-B643-C3060E9D343B", "Girls Shoes"),
    ("C7FEF0C8-C59D-44DC-9715-7C377441ECFE", "Baby's First Walkers"),
    ("54251EAE-F02B-4B6B-93D7-DE2BB387F60B", "Boys Clothing"),
    ("7BF9295D-69A0-483C-871C-9E3AF2A3496C", "Boy Jeans"),
    ("8DA1BB63-9FC2-4817-9271-3474CDBDDB30", "Boy T-Shirts"),
    ("BB0B0BAD-326B-4328-B1BF-319C420DF782", "Boy Hoodies & Sweatshirts"),
    ("BE16F1EB-5C31-4A1E-B80F-F1905F046E7F", "Outerwear & Coats"),
    ("C938C806-CB88-46AB-B782-89ECD0B25E25", "Boy Clothing Sets"),
    ("D91A4505-6495-4DFD-9984-C8E728913127", "Boy Accessories"),
    ("7A31FADF-137D-4C83-AD7B-BCF28CACDA94", "Baby Clothing"),
    ("04D82B39-7CF8-4CA5-ABC9-279181DE7E26", "Baby Clothing Sets"),
    ("80304DEB-99FB-4E29-9065-A99F732702C4", "Baby Rompers"),
    ("8F8C7970-3965-4EB6-8E13-ED77EB686DBA", "Baby Accessories"),
    ("A91DDCDF-A80E-40EE-ADB6-C3CB20CCB07E", "Baby Outerwear"),
    ("B34957D5-3AF6-4BE7-AC9F-72BAB8433CB6", "Baby Dresses"),
    ("B81FEFAC-C995-4665-8154-631E447F7236", "Baby Pants"),
    ("8C946349-0DC4-4B1E-AC41-E4FE30288DEE", "Baby & Mother"),
    ("0B08F5C8-0381-446D-A1C0-B90F69F45041", "Nappy Changing"),
    ("4065FFF7-4AAA-4CFA-B04B-639C93624469", "Activity & Gear"),
    ("5C374126-AE88-4617-B732-011174077E00", "Backpacks & Carriers"),
    ("77A1D79C-B67E-42C0-850F-00005042548C", "Baby Care"),
    ("CBAB567C-28EA-4916-97C9-786EEA80A3B8", "Maternity"),
    ("BE42B051-DE15-444A-97FA-79580E6AEC78", "Girls Clothing"),
    ("1357514957859721216", "Girls Underwear"),
    ("5795C34B-0DF0-4838-A78C-C125AA3BED18", "Family Matching Outfits"),
    ("5CC68C6B-8D69-41B2-838A-A98CB7DDD744", "Sleepwear & Robes"),
    ("6ED3E32C-89DD-4DD1-A991-FEAA4F3C1BFD", "Tops & Tees"),
    ("713CBA54-B38E-4C86-9323-1252113E437F", "Girl Clothing Sets"),
    ("88856603-65DA-419C-8C64-4C1E91A9E983", "Girl Accessories"),
    ("C421D769-76CC-4515-909E-4E7167EE6ABE", "Girl Dresses"),
    ("B8302697-CF47-4211-9BD0-DFE8995AEB30", "Men's Clothing"),
    ("20DA7E59-3A12-40DE-B8B6-78AD03A61DB1", "Underwear & Loungewear"),
    ("0222F963-84BC-4ED8-87A0-2EE6B7890B53", "Men's Sleep & Lounge"),
    ("12A1288F-063D-427F-BF07-10F53784849B", "Shorts"),
    ("1A3AF8F0-0549-4529-873A-5D109B301643", "Briefs"),
    ("60A76402-BF69-49A3-8FEC-28B9235BED62", "Robes"),
    ("A6A734F9-6F0B-4A9F-9ED4-0D35A9F5B877", "Man Pajama Sets"),
    ("AEEDE316-97ED-442D-AE77-3A444B1AF073", "Boxers"),
    ("E7F165D8-BBE8-4AE3-87E8-999864158243", "Long Johns"),
    ("609C16BC-2A1E-4FE5-9A07-7D7E36EA24F5", "Outerwear & Jackets"),
    ("007F26BA-B50A-4ADA-BD36-2CD341411230", "Suits & Blazer"),
    ("1357252400104214528", "Men's Sweaters"),
    ("1ED06BF8-F5D4-45E5-A95F-D7FC278C7EF3", "Genuine Leather"),
    ("222439DF-4ED5-4DCF-BB22-8FB41607C7D2", "Man Trench"),
    ("976399B4-534B-46F0-B18A-62075824A717", "Man Hoodies & Sweatshirts"),
    ("CD1AEB49-F87A-42D2-AD82-77708A8CDFD7", "Wool & Blends"),
    ("E6E0E866-DB80-4EC9-9557-578320427C34", "Parkas"),
    ("F7CF2C2C-A7F5-488B-B457-646028917DF2", "Down Jackets"),
    ("90619059-822F-469F-9231-D58761546093", "Accessories"),
    ("1C592A63-6E0F-4F25-9496-8BDD82BF4281", "Socks"),
    ("37F32196-21BB-49CE-B2D4-80787A5DF276", "Scarves"),
    ("44A3ADE0-A8EC-4101-A8DE-DF42F56EF3F1", "Man Gloves & Mittens"),
    ("C0EFBA18-A36D-48CD-B953-85DDFCB9B1C6", "Skullies & Beanies"),
    ("ECF5842F-2FE6-4DD7-8827-FAA8A1D3D199", "Belts"),
    ("EF619898-429D-49B6-BD66-49057C06259B", "Man Prescription Glasses"),
    ("ACCD31BE-6CFB-40DB-AB0D-FD5FAA14153A", "Bottoms"),
    ("758FE9DE-16D9-4860-8472-46C5BA460FF7", "Pajama Sets"),
    ("7D830BF3-03DB-4EBB-8A50-ED5F1231E17A", "Man Shorts"),
    ("846D76D8-095D-4DD8-89DF-1E48D869F60C", "Cargo Pants"),
    ("911754C0-443D-4ECF-9083-DF04C907BD81", "Man Jeans"),
    ("B97A0CAD-6160-485B-A3FD-04EE4493A442", "Harem Pants"),
    ("C992BFAB-12A9-4C61-A1DA-6E09C926BB81", "Casual Pants"),
    ("D75F1892-F6F8-4295-966B-CB405B77070A", "Sweatpants"),
    ("C118B8EA-D1AF-4C66-AA8A-FCCC28B8C073", "T-Shirts"),
    ("05B15AC3-931A-4A72-9F1D-DC54CBCA51C4", "Geometric"),
    ("521887E1-D6D5-4475-81B7-63B9F72DDFCA", "Striped"),
    ("655B8008-6BB9-4AA1-8025-6206ACFF018A", "Solid"),
    ("9E77F21D-54E4-41B5-BB97-2CECBEA9DA96", "3D"),
    ("BE11EEDB-B765-4A39-8A3D-F6015FC7A846", "Print"),
    ("CBD11BEF-8BA5-4C87-98DD-1A61192C0180", "Novelty & Special Use"),
    ("240F64DA-9C68-4C61-BDE5-33302BE84535", "Cosplay Costumes"),
    ("2B03202E-A4FF-414D-B027-7A0EE42F085F", "Stage & Dance Wear"),
    ("5CBE1FF8-3083-43DB-BBBF-81C301A9D5A8", "Exotic Apparel"),
    ("DC3A5713-984B-4877-95C4-8400B7151AF8", "Hats & Caps"),
    ("0203EC28-49AF-49E4-B899-333C0A235BD4", "Baseball Caps"),
    ("243C5278-C220-4110-B2AF-129118F09171", "Bomber Hats"),
    ("3F464061-C4C7-43FE-A3FE-84AD92838E56", "Berets"),
    ("EB891BA4-6F5C-4625-B76A-49504556B127", "Fedoras"),
    ("D9E66BF8-4E81-4CAB-A425-AEDEC5FBFBF2", "Consumer Electronics"),
    ("30063684-45E2-4929-BB85-441C1DF80DDE", "Accessories & Parts"),
    ("40CC2ED1-8998-4515-9139-787CC25D42A7", "Digital Cables"),
    ("599DFE31-C6AD-42D2-93AA-762126BBA475", "Home Electronic Accessories"),
    ("66D0D817-353B-492E-87A5-024091FF9000", "Audio & Video Cables"),
    ("6DB79FAF-593D-4F52-B6FF-AB1D14331862", "Charger"),
    ("A0D39205-3770-4F0B-91BD-65E711263577", "Batteries"),
    ("AD2B299F-EC10-4209-998A-8916AE4D4900", "Digital Gear Bags"),
    ("4BFAF763-DD09-4DD3-A7E9-E03724D1D51B", "Home Audio & Video"),
    ("0AC6B44A-12CC-456F-831F-54064C77D303", "Projectors"),
    ("0F932A8E-47CB-4CB6-B7C3-C4D9F7CF62EC", "Television"),
    ("3A557A5A-FDAF-48BF-A989-3ED90B9ED228", "TV Receivers"),
    ("872FA218-4F48-4F03-8FEE-ADE7CF21BC45", "Audio Amplifiers"),
    ("A9B643D0-7AA9-4703-A59B-D01C4526CDF9", "Projectors & Acessories"),
    ("D6C23AAE-B8EE-481C-9B61-34557971D45F", "Home Audio & Video"),
    ("D8515A8C-ECAC-422B-9963-14D7B07E10DB", "TV Sticks"),
    ("6A03FBB1-F7D9-441F-B06D-EF45CA87B553", "Smart Electronics"),
    ("11D33F89-9B90-4D1A-B977-DE229BAA7E86", "Wearable Devices"),
    ("36F73513-6A5A-445D-87F9-BF3D6629E649", "Smart Home Appliances"),
    ("4336FAFE-B9C9-4673-8706-BCFAE1448DA2", "Smart Wearable Accessories"),
    ("895CF515-0F6B-481D-8A32-604EDCBEFBED", "Smart Wristbands"),
    ("C83EF2A0-8FA3-4713-9901-2FD6E4554D97", "Smart Watches"),
    ("E95322D2-FF23-4837-A0C0-0CA686B9F062", "Smart Remote Controls"),
    ("85E0D3B7-C3C4-4F1B-98A6-958389A1BEBE", "Camera & Photo"),
    ("11D96803-A0A3-4175-B49B-2102EC285965", "Photo Studio"),
    ("907BBB40-C131-4D3C-BA05-794D47EEBC90", "Camera Drones"),
    ("A2B55BEF-9B7D-44A0-8E80-A14FFFBBBD94", "Camera & Photo Accessories"),
    ("AA40156F-A334-475E-9CA0-7E5520645980", "Digital Cameras"),
    ("AD21D6F7-42CB-44E7-89B2-542692C7D101", "Action Cameras"),
    ("DE5A9724-8B92-404F-B15E-1FCAD6594BAF", "Camcorders"),
    ("997DBFF0-627C-4397-80D3-C12EA3906969", "Video Games"),
    ("1F23F16D-0A39-4D38-AB9C-1F21EEDEBEDD", "Gamepads"),
    ("2F6CCFAA-853F-41EF-8B91-24028A333948", "Handheld Game Players"),
    ("56892B7E-0C59-4DAB-8336-57C6CA548043", "Video Game Consoles"),
    ("A8EBE688-6787-4ECF-8E5A-8802AC9C2135", "Stickers"),
    ("A96C59E8-C39A-4C8E-BA75-5B4AA347FCCC", "Joysticks"),
    ("DC11C779-CCD5-429C-9A93-F638456E745B", "Portable Audio & Video"),
    ("8FD4CA46-AA88-4CDC-8EBA-EBD8412152E2", "Microphones"),
    ("C1AB7563-AED4-44D8-9F01-05BD91C65307", "Speakers"),
    ("DAECCC3B-13D8-4978-86A8-61D3DF186134", "Earphones & Headphones"),
    ("EE64B306-1A1F-4879-A080-BF0ACA4400A9", "VR & AR Devices"),
    ("F34292A3-2774-4380-9ADF-78F90AB90863", "MP3 Players"),
    ("E9FDC79A-8365-4CA6-AC23-64D971F08B8B", "Phones & Accessories"),
    ("912FD088-248B-4D58-84F7-1F10B888CF8A", "Mobile Phone Accessories"),
    ("00134C46-B7DF-4500-A3D9-ABB7B779EFD0", "Cables"),
    ("491E5474-524C-4666-BDD7-4E35E38900EA", "Power Bank"),
    ("51D68796-F1B5-4BDC-B9E0-32C3D9FF6994", "Screen Protectors"),
    ("82643737-E055-4FDF-AD69-4E2C3FB6970B", "Lenses"),
    ("9170B3F9-5B9C-4C39-8CD6-7DC00E481D47", "Holders & Stands"),
    ("B200FABB-A76B-4750-9957-FEA3DCB21F1F", "Chargers"),
    ("9FA474CF-E06D-4708-AD56-F39FED7F88E3", "Cases & Covers"),
    ("0480D511-C923-4F7A-90F2-435F439DFE00", "Huawei Cases"),
    ("0B52E7DF-CBBD-4C4C-A43D-46B53056313C", "Patterned Cases"),
    ("1EE2EA4E-87BC-4108-BBF3-0A98A4A1EF89", "Cases For iPhone 6 & 6 Plus"),
    ("2CF32BF2-246D-4EC7-A060-6835C7EFD4AD", "Wallet Cases"),
    ("496A6FD1-4D2C-4E96-93B3-1BEBF5D7DA34", "Cases For iPhone 7 & 7 Plus"),
    ("4E8B1C9C-3126-4115-A5CA-357A8C164AD2", "Galaxy S8 Cases"),
    ("65AC23D3-BA63-438B-B8FE-71E117D717AF", "IPhone X Cases"),
    ("7CB75550-C920-47A8-8A65-27C34ED1C05E", "Galaxy S7 Cases"),
    ("7FD2D2BD-852D-4028-870E-AEB73594A95E", "Cases For iPhone 8 & 8 Plus"),
    ("948E69C1-D825-4797-B7F9-8D4FC69A20DA", "Xiaomi Cases"),
    ("C19F0351-2A98-43FF-BEA2-952BA6F75997", "Silicone Cases"),
    ("DD47EFC1-E65E-469A-94DA-658707A124B3", "Flip Cases"),
    ("E6C70353-4E58-4253-A840-3760667A9BE4", "Waterptoof Cases"),
    ("F77E8C4C-649A-4553-BD44-7604FADBB0BD", "Leather Cases"),
    ("BAD75444-1463-4B4C-8AD2-BC9ABDD92E5B", "Mobile Phone Parts"),
    ("14CC2DBB-21D3-4D3B-A263-75BF069ED074", "SIM Card & Tools"),
    ("2C46D1EB-148D-4DF3-8F23-EC0C5D5FDC1D", "Mobile Batteries"),
    ("3F222BC3-4864-487B-8E89-CE516D55638B", "Housings"),
    ("4C9F6BA4-70BB-49BC-A350-3D5E4E685B84", "LCDs"),
    ("5FE5E389-0B85-4592-A08D-B4AD79B164D4", "Flex Cables"),
    ("FF1E0375-F5BF-40D9-8B18-708F79D52E44", "Touch Panel"),
    ("F9AAF742-3A67-4887-BFBE-CF16B08910CF", "Mobile Phones"),
    ("0AADEC4E-024A-41DF-8801-4A0204F0E568", "Quad Core"),
    ("20278181-7942-4E22-B3CB-7CDFEE89297E", "Single SIM Card"),
    ("40FFAFDA-47CD-473A-B654-94D1923B15CF", "Dual SIM Card"),
    ("B1C9BC0B-A019-48C5-A06A-F25FB45DD9A9", "3GB RAM"),
    ("D0E7FF56-E94C-460D-8DB1-6695458475F4", "Octa Core"),
    ("F22F83A5-633C-4269-85A7-3FE844BD555F", "5-inch Display"),
]


marketplace_choices = [
    {'woocommerce','woo'},
    {'ebay', 'eby'}
]

class CJSearchProducts(forms.Form):
    pagenum = forms.IntegerField(label='Numero pagine',
                                            min_value=1,
                                            max_value=5,
                                            help_text='max 5',
                                            initial=1 , 
                                            widget=forms.NumberInput(attrs={'style': 'width: 300px; margin-top:0.5em;margin-bottom:1em',}))
    pagesize = forms.IntegerField(label='Risultati per pagina',
                                            min_value=20,
                                            max_value=200,
                                            help_text='min 20 - max 200',
                                            initial=20 , 
                                            validators=[MinValueValidator(1), MaxValueValidator(100)],
                                            widget=forms.NumberInput(attrs={'style': 'width: 300px; margin-top:0.5em;margin-bottom:1em',}))
    category = forms.TypedChoiceField(label='Select category',choices=cj_categories, initial='default',widget=forms.Select(attrs={'style': 'width: 220px;margin-bottom:2em'}))
    keywords = forms.CharField(label='Filter by keywords', max_length = 200, required=False)


class exportSetup(forms.Form):
    marketplace = forms.TypedChoiceField(label='Select marketplace',choices=marketplace_choices, initial='default',widget=forms.Select(attrs={'style': 'width: 220px;margin-bottom:2em'}))
    pricepercentageincrease = forms.FloatField(label="Increase price by (%):")
    selectcategories = forms.CharField(max_length = 200)

'''
import_options = (
    ("woocommerce","WooCommerce"),
    ("ebay","Ebay"),
    )

class ImportOptions(forms.Form):
    import_option = forms.TypedChoiceField(label='Import to:',choices=import_options, initial='woocommerce')

sync_options = (
    ("all", "All"),
    ("woocommerce","WooCommerce"),
    ("ebay","Ebay"),
    )

class SyncOptions(forms.Form):

manipulation_options = (
    ("edit", "Edit"),
    ("delete","Delete"),
    ("add-template","Add Template"),
    )

class ManipulationOptions(forms.Form):'''

class woocommerceImportSetup(forms.Form):
    pricepercentageincrease = forms.FloatField(label="Increase price by (%):")
    categories = forms.CharField(max_length = 200)

class EbayImportSetup(forms.Form):
    price_multiplier = forms.FloatField(label="Price Multiplier:", help_text=mark_safe("<div style='text-align:left'>Supplier price will be moltiplicated by this value. (i.e. If supplier price is 10 and multiplier 5, your sell price on Ebay will be 50.</div>"))

class newStoreWoocommerce(forms.Form):
    name = forms.CharField(max_length = 155, required=True)
    url = forms.CharField(max_length = 155, required=True)
    ck = forms.CharField(max_length = 155, required=True)
    cs = forms.CharField(max_length = 155, required=True)


class descriptionTemplate_1(forms.Form):
    title = forms.CharField(max_length = 100)
    urlimage1 = forms.CharField(max_length = 255)
    urlimage2 = forms.CharField(max_length = 255)
    urlimage3 = forms.CharField(max_length = 255)
    urlimage4 = forms.CharField(max_length = 255)
    urlimage5 = forms.CharField(max_length = 255)
    text1 = forms.CharField(max_length = 255)
    text2 = forms.CharField(max_length = 255)

class descriptionTemplate_2(forms.Form):
    title = forms.CharField(max_length = 100)
    generalDescription = forms.CharField(max_length = 255)
    urlimage1 = forms.CharField(max_length = 255)
    urlimage2 = forms.CharField(max_length = 255)
    text1 = forms.CharField(max_length = 255)
    text2 = forms.CharField(max_length = 255)

class EbayUpdateAccessTokenForm(forms.Form):
    access_token = forms.CharField(widget=forms.Textarea(attrs={
                    'class': "form-control",
                    'rows': 7, 
                    'style': 'max-width: 100%; font-size: 11px;',
                    }))

ECONOMY = "economy"
AVERAGE = "average"
GOOD = "good"
PREMIUM = "premium"

quality_choices = (
    (ECONOMY,"Economy"),
    (AVERAGE, "Average"),
    (GOOD, "Good"),
    (PREMIUM, "Premium"),
)

tone_of_voice_choices = (
    ("excited","Excited"),
    ("professional","Professional"),
    ("funny","Funny"),
    ("encouraging","Encouraging"),
    ("dramatic","Dramatic"),
    ("witty","Witty"),
    ("sarcastic","Sarcastic"),
    ("engaging","Engaging"),
    ("creative","Creative"),
)

class WritesonicDescriptionGeneratorForm(forms.Form):
    quality = forms.TypedChoiceField(label='Quality:',choices=quality_choices, initial='economy')
    tone_of_voice = forms.TypedChoiceField(label='Tone of voice:',choices=tone_of_voice_choices, initial='excited')
    primary_keyword = forms.CharField(max_length = 100, required=False, help_text='only with premium quality')
    secondary_keyword = forms.CharField(max_length = 100, required=False)
    keywords = forms.CharField(max_length = 100, required=False)
    num_copies = forms.IntegerField(max_value=3, min_value=1, initial=2)


prompt_description_options = (
    ("prompt-description-1","Excited"),
    ("prompt-2","Professional"),
    ("prompt-3","Funny"),
    ("prompt-4","Encouraging"),
)

prompt_title_options = (
    ("prompt-title-1","Excited"),
    ("prompt-2","Professional"),
    ("prompt-3","Funny"),
    ("prompt-4","Encouraging"),
)


model_options = (
    ("gpt-3.5-turbo","Gpt 3.5"),
    ("text-davinci-003","Da Vinci"),
    ("text-curie-001","Curie"),
    ("text-babbage-001","Babbage"),
    ("text-ada-001","Ada"),
)

class ChatGPTWriteDescriptionForm(forms.Form):
    prompt = forms.TypedChoiceField(label='Prompt:',choices=prompt_description_options, initial='prompt-description-1')
    model = forms.TypedChoiceField(label='Model:',choices=model_options, initial='gpt-3.5-turbo')
    keywords = forms.CharField(max_length = 100, required=False, help_text='write keywords separated by commas')
    min_words = forms.IntegerField(max_value=100, min_value=50, initial=70)
    max_words = forms.IntegerField(max_value=300, min_value=100, initial=120)
    rewrite_title = forms.BooleanField(label='Rewrite a SEO optimized title?',initial=False, required=False)

class ChatGPTAsk(forms.Form):
    question = forms.CharField(max_length = 250, required=True, help_text='Ask whatever you want')
    def __init__(self, *args, **kwargs):
        super(ChatGPTAsk, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['question'].label = False


class ChatGPTWriteTitleForm(forms.Form):
    prompt = forms.TypedChoiceField(label='Prompt:',choices=prompt_title_options, initial='prompt-title-1')
    model = forms.TypedChoiceField(label='Model:',choices=model_options, initial='text-davinci-003')
    keywords = forms.CharField(max_length = 100, required=False, help_text='write keywords separated by commas')

class InstagramPostSetup(forms.Form):
    caption = forms.CharField(label='Write a caption for your post:', help_text='2200 characters max', widget=forms.Textarea(attrs={
                                                    'maxlength':2200,
                                                    'class': "form-control",
                                                    'rows': 7, 
                                                    'style': 'max-width: 100%; font-size: 11px;',
                                                    }))
    use_woocommerce_description = forms.BooleanField(label='Use WooCommerce description?',initial=False, required=False, help_text='Use Woocommerce description')
    is_carousel = forms.BooleanField(label='Carousel Post?',initial=False, required=False, help_text='Check the box to create a carousel post (first 10 photos in the Woocommerce store will be used), otherwise only the main image will be used.')

class InventoryItemForm(ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['itemName', 'description', 'descriptionFeatures', 'supplier', 'sellPrice', 'brand','attributes','productImage','sku','supplierSellPrice','categoryFirst',
                    'materialNameEn','descriptionChatGpt']
        widgets = {
            'itemName': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 100%; font-size: 11px;',
                }),
            'sku': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 200px;  font-size: 11px;',
                'readonly': True,
                }),
            'supplier': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 200px;  font-size: 11px;',
                'readonly': True,
                }),
            'materialNameEn': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 200px;  font-size: 11px;',
                'readonly': True,
                }),
            'supplierSellPrice': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 200px; font-size: 11px;',
                'readonly': True,
                }),
            'categoryFirst' : TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 200px; font-size: 11px;',
                'readonly': True,
                }),
            'brand' : TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 200px; font-size: 11px;',
                }),
            'description': Textarea(attrs={
                    'class': "form-control",
                    'rows': 7, 
                    'style': 'max-width: 100%; font-size: 11px;',
                    }),
            'descriptionFeatures': Textarea(attrs={
                    'class': "form-control",
                    'rows': 7, 
                    'style': 'max-width: 100%; font-size: 11px;',
                    'blank':True,
                    }),
            'descriptionChatGpt': Textarea(attrs={
                    'class': "form-control",
                    'rows': 7, 
                    'style': 'max-width: 100%; font-size: 11px;',
                    }),
            'sellPrice': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 100%;font-size: 11px;',
                }),
            'attributes': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 200px;font-size: 11px;',
                'readonly': True,
                }),
            'productImage':TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 100%; font-size: 11px;',
                'readonly': True,
                }),
        }
    def __init__(self, *args, **kwargs):
        super(InventoryItemForm, self).__init__(*args, **kwargs)
        self.fields['descriptionFeatures'].required = False
    
class VariantForm(ModelForm):
    class Meta:
        model = Variant
        fields = ['variantNameEn', 'description','sellPrice', 'variantKey', 'variantSku','supplierSellPrice','variantImage','allShippingMethods','allLocations']
        widgets = {
            'variantNameEn': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 100%; font-size: 11px;',
                'placeholder': 'variantNameEn'
                }),
            
            'variantSku': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 100%; font-size: 11px;',
                'placeholder': 'variantNameEn',
                'readonly': True,
                }),
            'supplierSellPrice': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 100%; font-size: 11px;',
                'readonly': True,
                }),
            'sellPrice': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 100%; font-size: 11px;',
                'placeholder': 'variantNameEn',
                }),
            'description': Textarea(attrs={'cols': 100, 'rows': 2, 'style': 'max-width: 100%; font-size: 11px;',}),
            'variantKey': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 100%; font-size: 11px;',
                'placeholder': 'variantKey'
                }),
            'variantImage':TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 100%; font-size: 11px;',
                'readonly': True,
                }),
            'allShippingMethods':Textarea(attrs={'cols': 100, 'rows': 5, 'style': 'max-width: 100%; font-size: 11px;','readonly': True,}),
            'allLocations':Textarea(attrs={'cols': 100, 'rows': 5, 'style': 'max-width: 100%; font-size: 11px;','readonly': True,}),
        }