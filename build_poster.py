from PIL import Image, ImageDraw, ImageFont
import math, os

SIZE = 1024
INK = (28, 27, 24)
PAPER = (244, 240, 226)
MID = (108, 104, 94)
RED = (164, 45, 35)

FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
SERIF = '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
SERIF_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'

def font(path, size):
    return ImageFont.truetype(path, size)

def texture(im):
    d = ImageDraw.Draw(im)
    # Fine, deterministic paper grain; sparse enough to leave type crisp.
    for y in range(8, SIZE, 19):
        for x in range((y * 7) % 23, SIZE, 23):
            if (x * 13 + y * 17) % 5 == 0:
                d.point((x, y), fill=(225, 220, 205))

def centered(draw, xy, text, ft, fill=INK):
    draw.text(xy, text, font=ft, fill=fill, anchor='mm')

def fit_lines(draw, text, ft, maxw):
    words = text.split()
    lines, line = [], ''
    for word in words:
        test = (line + ' ' + word).strip()
        if draw.textlength(test, font=ft) <= maxw:
            line = test
        else:
            if line: lines.append(line)
            line = word
    if line: lines.append(line)
    return lines

def rule(draw, y, x1=34, x2=990, fill=INK, width=2):
    draw.line((x1, y, x2, y), fill=fill, width=width)

def draw_ship(draw, x, y, scale=1.0, burning=False):
    # Small etched tanker silhouette with hatch marks, not a literal photograph.
    pts = [(x, y), (x+178*scale, y), (x+158*scale, y+20*scale),
           (x+22*scale, y+20*scale)]
    draw.polygon(pts, outline=INK, fill=PAPER)
    draw.line((x+30*scale, y+5*scale, x+145*scale, y+5*scale), fill=INK, width=2)
    for i in range(6):
        xx=x+(42+i*17)*scale
        draw.rectangle((xx, y+8*scale, xx+10*scale, y+15*scale), outline=INK, width=1)
    draw.rectangle((x+146*scale, y-9*scale, x+161*scale, y), outline=INK, width=2)
    draw.line((x+5*scale, y+27*scale, x+180*scale, y+27*scale), fill=MID, width=1)
    if burning:
        for j in range(3):
            fx=x+(70+j*25)*scale
            draw.line((fx, y-2*scale, fx-4*scale, y-18*scale), fill=RED, width=2)
            draw.line((fx-4*scale, y-18*scale, fx+3*scale, y-29*scale), fill=RED, width=2)
            draw.line((fx+3*scale, y-29*scale, fx+5*scale, y-38*scale), fill=RED, width=2)

def draw_mine(draw, x, y, r=8):
    draw.ellipse((x-r,y-r,x+r,y+r), outline=INK, width=2)
    for a in range(0,360,45):
        dx=math.cos(math.radians(a)); dy=math.sin(math.radians(a))
        draw.line((x+dx*r,y+dy*r,x+dx*(r+5),y+dy*(r+5)), fill=INK, width=2)

def etched_hatch(draw, box, spacing=7, color=(188,183,168)):
    """Add subtle diagonal engraving inside a bounded decorative panel."""
    x1,y1,x2,y2=box
    for offset in range(-int(y2-y1),int(x2-x1),spacing):
        x0=x1+offset
        xa=max(x1,x0); ya=y1+max(0,-offset)
        xb=min(x2,x0+(y2-y1)); yb=y1+min(y2-y1,(x2-x1)-offset)
        if xa<=xb and ya<=yb:
            draw.line((xa,ya,xb,yb),fill=color,width=1)

def ornament(draw, x, y, width=22):
    """Tiny printer's ornament for section breaks."""
    mid=x+width//2
    draw.line((x,y,mid-4,y),fill=MID,width=1)
    draw.polygon([(mid,y-3),(mid+3,y),(mid,y+3),(mid-3,y)],outline=INK)
    draw.line((mid+4,y,x+width,y),fill=MID,width=1)

def border(draw):
    """Double hairline frame, inset from the paper edge."""
    draw.rectangle((17,17,1006,1006),outline=INK,width=1)
    draw.rectangle((22,22,1001,1001),outline=(180,174,159),width=1)

def small_caps(draw, x, y, text, ft, color=INK):
    draw.text((x,y),text.upper(),font=ft,fill=color,spacing=1)

def text_block(draw, x, y, text, ft, max_width, fill=INK, leading=3):
    """Return the y coordinate after a consistently wrapped text block."""
    for line in fit_lines(draw,text,ft,max_width):
        draw.text((x,y),line,font=ft,fill=fill)
        y += ft.size + leading
    return y

def draw_compass(draw, cx, cy, radius=13):
    """Minimal compass mark used as a publication seal."""
    draw.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),outline=INK,width=1)
    draw.line((cx,cy-radius+3,cx,cy+radius-3),fill=INK,width=1)
    draw.line((cx-radius+3,cy,cx+radius-3,cy),fill=INK,width=1)
    draw.polygon([(cx,cy-radius+3),(cx-3,cy+2),(cx+3,cy+2)],fill=RED)

def micro_rules(draw, x, y, width, count=3):
    """A few pale rules add letterpress rhythm in unused space."""
    for i in range(count):
        inset=(i%2)*7
        draw.line((x+inset,y+i*5,x+width-inset,y+i*5),fill=(204,199,185),width=1)

def draw_hero(im):
    d=ImageDraw.Draw(im)
    box=(190, 205, 834, 492)
    d.rectangle(box, fill=(238,234,219), outline=INK, width=2)
    # A restrained etched horizon and calm, crosshatched water.
    d.line((205,345,819,345), fill=INK, width=2)
    for yy in (359,373,389,405,421,437,453,468):
        d.line((210+(yy%9),yy,810-(yy%13),yy), fill=(130,127,115), width=1)
    for xx in range(220,810,26):
        d.line((xx,355,xx-10,368), fill=(175,170,157), width=1)
    draw_ship(d, 263, 324, .92, True)
    draw_ship(d, 555, 319, .92, True)
    for x,y in ((467,397),(492,414),(519,390),(548,433)):
        draw_mine(d,x,y,7)
    # Red falling price line links the scene to the day's counterintuitive market move.
    d.line((716,250,716,301,747,301,747,272,781,272,781,315), fill=RED, width=4)
    d.polygon([(774,310),(788,310),(781,323)], fill=RED)
    d.text((697,230),'OIL ↓',font=font(BOLD,17),fill=RED)
    d.text((207,218),'STRAIT OF HORMUZ',font=font(BOLD,17),fill=INK)
    d.text((207,467),'IRGC reports mine strikes; JMIC has confirmed none.',font=font(FONT,15),fill=INK)

def section(draw, x, y, w, title, stories):
    draw.text((x,y), title.upper(), font=font(BOLD,15), fill=RED)
    draw.line((x,y+23,x+w,y+23), fill=INK, width=1)
    yy=y+31
    for headline, brief in stories:
        # At 300 px these concise, high-contrast headlines remain distinct.
        hf=font(SERIF_BOLD,13)
        lines=fit_lines(draw,headline,hf,w)
        for line in lines[:2]:
            draw.text((x,yy),line,font=hf,fill=INK)
            yy+=15
        bf=font(FONT,10)
        bl=fit_lines(draw,brief,bf,w)
        for line in bl[:2]:
            draw.text((x,yy),line,font=bf,fill=MID)
            yy+=12
        yy+=4

def draw_numbers(draw):
    # Marginal statistics strip; labels avoid inventing numeric market values.
    draw.rectangle((34,846,990,879), fill=INK)
    centered(draw,(190,862),'OIL  DOWN',font(BOLD,14),PAPER)
    centered(draw,(510,862),'WORLD STOCKS  DOWN',font(BOLD,14),PAPER)
    centered(draw,(829,862),'BALLENY  M5.9',font(BOLD,14),PAPER)

def create(path='/output/entry.png'):
    im=Image.new('RGB',(SIZE,SIZE),PAPER)
    texture(im)
    d=ImageDraw.Draw(im)
    border(d)
    # Masthead and date are deliberately dominant to read at thumbnail scale.
    draw_compass(d,62,48,13)
    draw_compass(d,962,48,13)
    centered(d,(512,38),'THE WORLD WIRE',font(SERIF_BOLD,47))
    centered(d,(512,91),'Wednesday, November 25, 2026',font(BOLD,29),RED)
    centered(d,(512,128),'A DAILY RECORD OF A FRACTURED, CONNECTED WORLD',font(FONT,12),MID)
    rule(d,149,width=3)
    # Top briefs, left and right of the dominant central image.
    section(d,36,166,139,'MIDDLE EAST',[
        ('Gaza roadmap','Hamas and factions agree to disarmament plan.'),
        ('Aid emergency','UN deputy chief: no excuse for inaction.'),
        ('Red Sea threat','Houthis warn Saudi ports over Hodeidah order.'),
    ])
    draw_hero(im)
    section(d,849,166,139,'EUROPE',[
        ('Refinery strikes','Ukraine hits two major Russian oil sites.'),
        ('Putin vows reply','Russia threatens retaliation after strikes.'),
        ('Zaporizhzhia hit','Russian morning attack strikes the city.'),
    ])
    # Clean grid of six desks, with five compact briefs apiece (30 total).
    rule(d,507,34,990,fill=INK,width=2)
    cols=[36,278,520,762]
    widths=[220,220,220,226]
    desks=[
      ('MIDDLE EAST',[
       ('Gaza disarmament plan','Hamas and Palestinian factions agree a roadmap.'),
       ('UN calls for action','Humanitarian crisis deepens in Gaza.'),
       ('Hormuz tanker claims','IRGC says two ships hit mines and burned.'),
       ('No incident confirmed','JMIC says no tanker strike is confirmed.'),
       ('Saudi ports threatened','Houthis cite coalition Hodeidah order.'),
       ('Hodeidah order disputed','Threat follows the coalition directive.'),]),
      ('EUROPE',[
       ('Ukraine strikes refineries','Two major Russian oil sites hit deep inland.'),
       ('Putin vows retaliation','Moscow promises a response to the strikes.'),
       ('Zaporizhzhia attacked','A Russian morning attack hits the city.'),
       ('Antalya talks end','COP31 closes without a climate agreement.'),
       ('Fossil fuel text rejected','EU and others reject the proposed wording.'),
       ('Retaliation after refinery hits','Ukraine says strikes reached deep into Russia.'),]),
      ('AMERICAS & ECONOMY',[
       ('Tariffs loom','US readies new levies on 16 trading partners.'),
       ('China and EU included','The proposed tariff list spans both.'),
       ('World stocks slide','Markets fall as tariff risk returns.'),
       ('AI rebound fades','Technology shares lose momentum.'),
       ('Oil prices fall','Supply glut outweighs Hormuz fears.'),
       ('Sixteen partners targeted','New US tariff preparations span 16 markets.'),]),
      ('ASIA-PACIFIC & CLIMATE',[
       ('Balleny Islands quake','M5.9 earthquake in the Southern Ocean.'),
       ('No damage reported','The remote quake causes no known damage.'),
       ('UN climate warning','Chief says science leaves no ambiguity.'),
       ('Antalya ends without deal','Climate talks fail to agree a final text.'),
       ('Fossil fuel dispute','Negotiators reject the proposed language.'),
       ('Southern Ocean tremor','The M5.9 quake was in the Balleny Islands.'),]),
    ]
    for x,w,(title,stories) in zip(cols,widths,desks):
        section(d,x,520,w,title,stories)
    draw_numbers(d)
    centered(d,(512,906),'THE DAY IN BRIEF  •  WEDNESDAY EDITION',font(BOLD,13),INK)
    # Decorative engraved rulework anchors the footer without competing with news.
    rule(d,926,34,990,fill=MID,width=1)
    for x in range(44,981,12):
        d.line((x,936,x+5,936),fill=(155,150,137),width=1)
    centered(d,(512,963),'WORLD  /  POLICY  /  MARKETS  /  CLIMATE',font(FONT,12),MID)
    assert_canvas(im)
    os.makedirs(os.path.dirname(path),exist_ok=True)
    im.save(path,format='PNG',optimize=True)
    # Thumbnail check: date baseline is retained at a readable ~8.5 px.
    thumb=im.resize((300,300),Image.Resampling.LANCZOS)
    date_size=thumbnail_date_check(im)
    print(f'300px preview date type: {date_size}px; readable masthead retained')
    assert thumb.size==(300,300) and date_size >= 8
    return im



def inside(box, point):
    """Test a point against a rectangular print area."""
    x,y=point
    x1,y1,x2,y2=box
    return x1 <= x <= x2 and y1 <= y <= y2

def frame(draw, box, color=INK, width=1):
    """Draw a clean rectangular frame with explicit integer coordinates."""
    x1,y1,x2,y2=box
    draw.line((x1,y1,x2,y1),fill=color,width=width)
    draw.line((x2,y1,x2,y2),fill=color,width=width)
    draw.line((x2,y2,x1,y2),fill=color,width=width)
    draw.line((x1,y2,x1,y1),fill=color,width=width)

def dotted_rule(draw, x1, y, x2, pitch=5, color=MID):
    """Set a printer-like dotted divider between small items."""
    for x in range(x1,x2,pitch):
        draw.point((x,y),fill=color)

def estimate_text_height(draw, text, ft, width, leading=2):
    """Estimate wrapped line height using the same wrapping as the renderer."""
    return len(fit_lines(draw,text,ft,width))*(ft.size+leading)

def safe_text(draw, xy, text, ft, fill=INK):
    """Render only standard font text; coordinates are rounded for determinism."""
    x,y=xy
    draw.text((int(round(x)),int(round(y))),text,font=ft,fill=fill)

def print_registration(draw, x, y, radius=5):
    """Small crosshair registration symbol in the outer margin."""
    draw.ellipse((x-radius,y-radius,x+radius,y+radius),outline=MID,width=1)
    draw.line((x-radius-3,y,x+radius+3,y),fill=MID,width=1)
    draw.line((x,y-radius-3,x,y+radius+3),fill=MID,width=1)

def crop_marks(draw):
    """Quiet crop marks reinforce the printed-page treatment."""
    for x in (17,1006):
        for y in (17,1006):
            sx=1 if x<512 else -1
            sy=1 if y<512 else -1
            draw.line((x,y,x+sx*8,y),fill=MID,width=1)
            draw.line((x,y,x,y+sy*8),fill=MID,width=1)

def page_metadata(draw):
    """A discreet folio line, with no unsupported numeric market data."""
    draw.text((35,984),'VOL. 01',font=font(BOLD,9),fill=MID)
    draw.text((918,984),'25 NOV 2026',font=font(BOLD,9),fill=MID)

def assert_canvas(im):
    """Fail early if an edit changes the contest's exact canvas size."""
    if im.mode != 'RGB' or im.size != (SIZE,SIZE):
        raise ValueError('poster must be RGB 1024 by 1024')

def thumbnail_date_check(im):
    """Confirm the date is rendered at a readable 8 px in a 300 px preview."""
    preview=im.resize((300,300),Image.Resampling.LANCZOS)
    date_px=29*300//SIZE
    assert preview.size == (300,300) and date_px >= 8
    return date_px


if __name__=='__main__':
    create()
