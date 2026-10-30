import glob, json, os, re, sys
import pymupdf

ROOT = "E:/__고1_2학기"
OUT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(OUT, "sources")
ROMAN = {"Ⅰ": "1", "Ⅱ": "2", "Ⅲ": "3", "Ⅳ": "4", "Ⅴ": "5"}


def uid(code):
    for r, a in ROMAN.items():
        code = code.replace(r, a)
    return re.sub(r"[^0-9A-Za-z-]", "", code.replace("(", "-").replace(")", ""))


def cut_pdf(pdf, a, b, path):
    if os.path.exists(path):
        return
    d = pymupdf.open(pdf)
    o = pymupdf.open()
    o.insert_pdf(d, from_page=a - 1, to_page=b - 1)
    o.save(path, garbage=3, deflate=True)


def subject(sid, name, book, units):
    os.makedirs(os.path.join(SRC, sid), exist_ok=True)
    return {"id": sid, "name": name, "book": book, "units": units}


def social():
    pdf = f"{ROOT}/통합사회/비상_통합사회2_학생용 교과서.pdf"
    toc = pymupdf.open(pdf).get_toc()
    ch = sec = None
    marks = []
    for lvl, t, p in toc:
        t = re.sub(r"<[^>]+>", "", t).strip()
        if lvl == 1:
            ch = t
            if t == "부록":
                marks.append((None, None, None, p))
                break
        elif lvl == 2:
            sec = t
            marks.append((None, None, None, p))
        elif lvl == 3 and re.match(r"^\d\.", t):
            marks.append((ch, sec, t, p))
    units = []
    real = [m for m in marks if m[2]]
    for m in real:
        i = marks.index(m)
        end = marks[i + 1][3] - 1 if i + 1 < len(marks) else m[3] + 3
        roman = m[0].split(".")[0]
        sn = m[1].split(".")[0]
        n = m[2].split(".")[0]
        code = f"{roman}-{sn}-{n}"
        u = uid(code)
        path = f"sources/social/{u}.pdf"
        cut_pdf(pdf, m[3], end, os.path.join(OUT, path))
        units.append({"id": u, "code": code, "chapter": m[0], "section": m[1], "title": m[2].split(". ", 1)[1], "pages": f"{m[3]}-{end}", "source": path})
    return subject("social", "통합사회", "비상 통합사회2", units)


SCI = [("Ⅰ-1-01", "지질 시대의 환경과 생물의 변화", 14, 21), ("Ⅰ-1-02", "자연선택과 생물의 진화", 22, 27), ("Ⅰ-1-03", "생물다양성과 보전 방안", 28, 31),
       ("Ⅰ-2-01", "산화·환원 반응의 규칙성", 38, 43), ("Ⅰ-2-02", "생활 주변의 산화·환원 반응", 44, 47), ("Ⅰ-2-03", "산과 염기의 종류와 성질", 48, 53),
       ("Ⅰ-2-04", "중화 반응과 실생활 이용", 54, 59), ("Ⅰ-2-05", "물질 변화에서 에너지 출입", 60, 63), ("Ⅱ-1-01", "생태계 구성요소와 상호작용", 74, 79),
       ("Ⅱ-1-02", "생태계평형과 생태계보전", 80, 85), ("Ⅱ-1-03", "온실 효과와 지구 온난화", 86, 89), ("Ⅱ-1-04", "지구 환경 변화와 우리 생활", 90, 95),
       ("Ⅱ-2-01", "지구의 에너지원, 태양 에너지", 102, 103), ("Ⅱ-2-02", "전기 에너지 생산과 발전기", 104, 107), ("Ⅱ-2-03", "화력·핵발전의 영향", 108, 111),
       ("Ⅱ-2-04", "에너지 전환과 효율적 이용", 112, 117), ("Ⅱ-2-05", "신재생 에너지 기술 활용", 118, 121), ("Ⅲ-1-01", "미래 사회 문제 해결과 과학", 132, 137),
       ("Ⅲ-1-02", "빅데이터와 과학기술사회", 138, 143), ("Ⅲ-1-03", "과학기술의 발전과 우리 생활", 144, 147), ("Ⅲ-1-04", "과학 관련 사회적 쟁점과 윤리", 148, 151)]

KOR = [("1-(1)", "사회적 독서 활동에 참여하기", 12, 19), ("1-(2)", "주제 통합적 읽기와 논증하는 글 쓰기", 20, 36), ("2-(1)", "옛 노래의 향기", 44, 51),
       ("2-(2)", "옛이야기의 즐거움", 52, 68), ("2-(3)", "현대 시의 시선", 69, 75), ("2-(4)", "현대 소설의 빛깔", 76, 95),
       ("3-(1)", "함께 만족하는 협상", 100, 111), ("3-(2)", "작문 관습을 고려한 글쓰기", 112, 124), ("4-(1)", "국어가 걸어온 길", 130, 139),
       ("4-(2)", "바르고 정확한 국어생활", 140, 153), ("4-(3)", "매체와 함께하는 생활", 154, 167), ("5-(1)", "주체적이고 비판적인 매체 비평", 172, 183),
       ("5-(2)", "복합양식의 글 읽기와 쓰기", 184, 200)]

ENG = [("L1", "Make Your World a Better Place", 8, 31), ("L2", "From Tradition to Trend", 32, 55), ("L3", "Beyond Barriers", 56, 79), ("L4", "The Essence of Being Human", 80, 105)]

INFO = [("Ⅱ-01", "디지털 데이터 압축", 35, 47, 2), ("Ⅱ-02", "디지털 데이터 암호화", 48, 53, 2), ("Ⅱ-03", "빅데이터 개념과 분석", 54, 74, 2),
        ("Ⅲ-01", "문제 분해와 모델링", 75, 91, 3), ("Ⅲ-02", "알고리즘", 92, 107, 3), ("Ⅲ-03", "프로그래밍의 이해", 108, 123, 3),
        ("Ⅲ-04", "제어 구조의 응용", 124, 137, 3), ("Ⅲ-05", "함수와 라이브러리", 138, 151, 3), ("Ⅲ-06", "객체지향 프로그래밍", 152, 159, 3),
        ("Ⅲ-07", "창의 융합 프로그래밍", 160, 168, 3), ("Ⅳ-01", "인공지능과 지능 에이전트", 169, 179, 4), ("Ⅳ-02", "기계학습의 개념", 180, 183, 4),
        ("Ⅳ-03", "기계학습의 모델과 구현", 184, 208, 4), ("Ⅴ-01", "디지털 사회와 진로", 209, 219, 5), ("Ⅴ-02", "정보 보호와 보안", 220, 236, 5)]
INFO_FILES = {2: "2_데이터", 3: "3_알고리즘과프로그래밍", 4: "4_인공지능", 5: "5_디지털문화"}
PILOT = [("1-01a", "Ⅰ-01a", "유선·무선 네트워크의 특성과 무선 기술", "7-13", "U1"), ("1-01b", "Ⅰ-01b", "인터넷 네트워크 연결과 네트워크에서의 공유", "14-17", "U2"),
         ("1-02a", "Ⅰ-02a", "사물 인터넷의 구성·기술·사회 변화", "18-22", "U3"), ("1-02b", "Ⅰ-02b", "마이크로비트로 사물 인터넷 실습과 문제 해결", "23-34", "U4")]


def pdf_list(sid, pdf, rows):
    units = []
    for code, title, a, b in rows:
        u = uid(code)
        path = f"sources/{sid}/{u}.pdf"
        cut_pdf(pdf, a, b, os.path.join(OUT, path))
        units.append({"id": u, "code": code, "title": title, "pages": f"{a}-{b}", "source": path})
    return units


def info():
    units = [{"id": u, "code": c, "title": t, "pages": p, "imported": pilot} for u, c, t, p, pilot in PILOT]
    for code, title, a, b, f in INFO:
        txt = open(f"{ROOT}/정보/_src/{INFO_FILES[f]}.txt", encoding="utf-8").read()
        parts = re.split(r"=====P(\d+)=====", txt)
        pages = {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}
        body = "\n".join(f"[교과서 {p}쪽]\n{pages[p].strip()}" for p in range(a, b + 1) if p in pages)
        if not body:
            print("EMPTY info", code, file=sys.stderr)
            continue
        u = uid(code)
        path = f"sources/info/{u}.txt"
        open(os.path.join(OUT, path), "w", encoding="utf-8").write(f"고등학교 정보(천재교육, 김현철) {code} {title} (교과서 {a}~{b}쪽)\n\n{body}\n")
        units.append({"id": u, "code": code, "title": title, "pages": f"{a}-{b}", "source": path})
    return subject("info", "정보", "천재 정보", units)


def math():
    units = []
    for f in sorted(glob.glob(f"{ROOT}/수학/천재_공통수학2_소단원별/*.pdf")):
        m = re.match(r"\d+_([ⅠⅡⅢ]-\d-\d{2})_(.+?) \(p(\d+)-(\d+)\)\.pdf$", os.path.basename(f))
        if not m:
            continue
        code, title, a, b = m.group(1), m.group(2), int(m.group(3)), int(m.group(4))
        u = uid(code)
        path = f"sources/math/{u}.pdf"
        if not os.path.exists(os.path.join(OUT, path)):
            pymupdf.open(f).save(os.path.join(OUT, path), garbage=3, deflate=True)
        units.append({"id": u, "code": code, "title": title.replace("_", " "), "pages": f"{a}-{b}", "source": path})
    return subject("math", "수학", "천재 공통수학2", units)


for s in ("social", "science", "info", "korean", "english", "math"):
    os.makedirs(os.path.join(SRC, s), exist_ok=True)
subs = [social()]
os.makedirs(os.path.join(SRC, "science"), exist_ok=True)
subs.append(subject("science", "통합과학", "천재 통합과학2", pdf_list("science", f"{ROOT}/통합과학/천재_고등_통합과학2(신영준)_교과서.pdf", SCI)))
subs.append(info())
os.makedirs(os.path.join(SRC, "korean"), exist_ok=True)
subs.append(subject("korean", "국어", "지학사 공통국어2", pdf_list("korean", glob.glob(f"{ROOT}/국어/*지학사*교과서*.pdf")[0], KOR)))
os.makedirs(os.path.join(SRC, "english"), exist_ok=True)
subs.append(subject("english", "영어", "YBM 공통영어2", pdf_list("english", glob.glob(f"{ROOT}/영어/고등 공통영어2*교과서*.pdf")[0], ENG)))
subs.append(math())
json.dump({"subjects": subs}, open(os.path.join(OUT, "catalog.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for s in subs:
    print(s["id"], len(s["units"]), "units", s["units"][0]["code"], "..", s["units"][-1]["code"])
tot = sum(os.path.getsize(p) for p in glob.glob(os.path.join(SRC, "*", "*")))
print("sources MB", round(tot / 1e6, 1))
