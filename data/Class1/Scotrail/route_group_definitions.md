# ScotRail Route Group Definitions

## Purpose

Defines the route groups used within the ScotRail network dataset for The Route and Routepedia.

Route groups represent operational corridors and service identities rather than individual train services.

Stations may belong to more than one route group where appropriate.

---

## Edinburgh–Glasgow Main Line

### Purpose

The principal inter-city corridor linking Scotland's two largest cities via Falkirk High.

### Core Route

Edinburgh Waverley
Haymarket
Linlithgow
Polmont
Falkirk High
Croy
Lenzie
Glasgow Queen Street

### Can Overlap With

* Highland Main Line
* Stirling Corridor

---

## Shotts Line

### Purpose

Alternative route between Glasgow Central and Edinburgh via Lanarkshire and West Lothian.

### Core Route

Glasgow Central
Bellshill
Shotts
West Calder
Livingston South
Edinburgh Waverley

### Can Overlap With

* Argyle Line
* Lanark Line

---

## Carstairs Corridor

### Purpose

Main line linking Glasgow and Edinburgh via Motherwell and Carstairs.

### Core Route

Glasgow Central
Motherwell
Carstairs
Haymarket
Edinburgh Waverley

### Can Overlap With

* Lanark Line
* Borders Railway

---

## Highland Main Line

### Purpose

Principal Highland route linking Perth with Inverness.

### Core Route

Perth
Pitlochry
Blair Atholl
Dalwhinnie
Kingussie
Aviemore
Carrbridge
Inverness

### Can Overlap With

* Edinburgh–Glasgow Main Line
* Aberdeen Line

---

## Aberdeen Line

### Purpose

East Coast corridor linking Edinburgh with Aberdeen.

### Core Route

Edinburgh Waverley
Leuchars
Dundee
Arbroath
Montrose
Stonehaven
Aberdeen

### Can Overlap With

* Fife Circle
* Highland Main Line

---

## Fife Circle

### Purpose

Circular commuter network serving Fife between Edinburgh and Dundee.

### Core Route

Inverkeithing
Rosyth
Dunfermline
Cowdenbeath
Kirkcaldy
Markinch
Ladybank
Leuchars

### Can Overlap With

* Aberdeen Line

---

## Borders Railway

### Purpose

Route linking Edinburgh with the Scottish Borders.

### Core Route

Edinburgh Waverley
Brunstane
Shawfair
Eskbank
Newtongrange
Gorebridge
Stow
Galashiels
Tweedbank

### Can Overlap With

* Carstairs Corridor

---

## West Highland Line

### Purpose

Scenic Highland route linking Glasgow with Fort William and Mallaig.

### Core Route

Glasgow Queen Street
Helensburgh Upper
Crianlarich
Bridge of Orchy
Rannoch
Corrour
Fort William
Mallaig

### Can Overlap With

* Oban Branch

---

## Oban Branch

### Purpose

Branch from Crianlarich to Oban.

### Core Route

Crianlarich
Tyndrum Lower
Dalmally
Taynuilt
Connel Ferry
Oban

### Can Overlap With

* West Highland Line

---

## Far North Line

### Purpose

Northern route from Inverness to Wick and Thurso.

### Core Route

Inverness
Dingwall
Tain
Golspie
Brora
Helmsdale
Georgemas Junction
Thurso
Wick

### Can Overlap With

None

---

## Kyle Line

### Purpose

Scenic route linking Inverness with Kyle of Lochalsh.

### Core Route

Inverness
Dingwall
Achnasheen
Strathcarron
Plockton
Kyle of Lochalsh

### Can Overlap With

None

---

## Ayrshire Coast

### Purpose

Principal southwest commuter corridor.

### Core Route

Glasgow Central
Paisley Gilmour Street
Irvine
Kilwinning
Prestwick
Ayr

### Can Overlap With

* Largs Branch
* Ardrossan Branch

---

## Largs Branch

### Purpose

Branch serving the North Ayrshire coast.

### Core Route

Kilwinning
West Kilbride
Fairlie
Largs

### Can Overlap With

* Ayrshire Coast

---

## Ardrossan Branch

### Purpose

Branch serving Ardrossan Harbour and ferry connections.

### Core Route

Kilwinning
Ardrossan South Beach
Ardrossan Town
Ardrossan Harbour

### Can Overlap With

* Ayrshire Coast

---

## Inverclyde Line

### Purpose

Routes serving Greenock and Gourock.

### Core Route

Glasgow Central
Paisley Gilmour Street
Port Glasgow
Greenock Central
Gourock

### Can Overlap With

* Wemyss Bay Branch

---

## Wemyss Bay Branch

### Purpose

Branch serving Wemyss Bay ferry terminal.

### Core Route

Port Glasgow
IBM
Wemyss Bay

### Can Overlap With

* Inverclyde Line

---

## Cathcart Circle

### Purpose

Dense suburban circular network south of Glasgow.

### Core Route

Glasgow Central
Mount Florida
Cathcart
Langside
Pollokshields East
Glasgow Central

### Can Overlap With

* Neilston Line
* Newton Line

---

## Neilston Line

### Purpose

Suburban branch to Neilston.

### Core Route

Glasgow Central
Pollokshaws West
Kennishead
Neilston

### Can Overlap With

* Cathcart Circle

---

## Newton Line

### Purpose

Suburban route from Glasgow to Newton.

### Core Route

Glasgow Central
Mount Florida
Croftfoot
Kings Park
Newton

### Can Overlap With

* Cathcart Circle

---

## East Kilbride Line

### Purpose

Route serving East Kilbride.

### Core Route

Glasgow Central
Busby
Hairmyres
East Kilbride

### Can Overlap With

None

---

## Argyle Line

### Purpose

Cross-city route linking Milngavie, Glasgow Low Level and Lanarkshire.

### Core Route

Milngavie
Partick
Glasgow Central Low Level
Bellshill
Motherwell

### Can Overlap With

* Shotts Line
* Lanark Line

---

## Lanark Line

### Purpose

Branch serving Lanark.

### Core Route

Motherwell
Shieldmuir
Wishaw
Carluke
Lanark

### Can Overlap With

* Argyle Line
* Carstairs Corridor

---

## Stranraer Line

### Purpose

Southwest rural route linking Ayr with Stranraer.

### Core Route

Ayr
Girvan
Barrhill
Stranraer

### Can Overlap With

None

---

## Membership Principles

* Stations may belong to multiple route groups.
* Route groups represent operational corridors rather than individual train services.
* Scenic routes are treated as operational route groups.
* Glasgow suburban branches normally retain their own route group.
* Long-distance Highland corridors are maintained separately for gameplay.
* Route group definitions may be reviewed as gameplay evolves.

## Completion Status

### Dataset

- [ ] Station list validated
- [ ] Regions assigned
- [ ] Route groups assigned
- [ ] Scenic route flag assigned
- [ ] Coastal flag assigned
- [ ] Difficulty scoring assigned
- [ ] Accessibility scoring assigned
- [ ] Interchange classification assigned

### Coverage

- [ ] 363 of 363 stations assigned to at least one route group
- [ ] No unclassified stations remain

### Automation

- [ ] Route groups generated from station-name definitions
- [ ] scotrail.json is the source of truth
- [ ] No manual CRS maintenance required

### Future

- [ ] Routepedia content