import json
import urllib.request

BENCHMARK_TEST_CASES = [
    # --- DOMAIN 1: HOURS OF WORK, OVERTIME, MEAL BREAKS & NIGHT SHIFT ---
    {"test_id": "TC-001", "query": "Ilang oras ba talaga ang legal na trabaho sa isang araw?", "expected_article": "Art. 83"},
    {"test_id": "TC-002", "query": "What are the normal hours of work per day for private employees?", "expected_article": "Art. 83"},
    {"test_id": "TC-003", "query": "Pinagtatrabaho kami ng 10 hours daily, may bayad ba ang sobra sa 8 hours?", "expected_article": "Art. 87"},
    {"test_id": "TC-004", "query": "How is overtime pay computed under the labor code?", "expected_article": "Art. 87"},
    {"test_id": "TC-005", "query": "Pwede bang pilitin ng employer ang worker na mag-overtime kapag emergency?", "expected_article": "Art. 89"},
    {"test_id": "TC-006", "query": "Emergency overtime work exceptions and compulsory overtime conditions", "expected_article": "Art. 89"},
    {"test_id": "TC-007", "query": "May karapatan ba sa meal break ang empleyado sa buong araw na shift?", "expected_article": "Art. 85"},
    {"test_id": "TC-008", "query": "How long is the mandatory meal period for regular workers?", "expected_article": "Art. 85"},
    {"test_id": "TC-009", "query": "Nagtatrabaho ako mula alas diyes ng gabi hanggang umaga may dagdag ba?", "expected_article": "Art. 86"},
    {"test_id": "TC-010", "query": "What is night shift differential pay and coverage hours?", "expected_article": "Art. 86"},
    {"test_id": "TC-011", "query": "Kinaltas ng boss ang undertime ko sa naipon kong overtime kahapon legal ba?", "expected_article": "Art. 88"},
    {"test_id": "TC-012", "query": "Can undertime work be offset by overtime on another day?", "expected_article": "Art. 88"},
    {"test_id": "TC-013", "query": "Kasama ba sa bilang ng oras ng trabaho kapag naghihintay ng task on duty?", "expected_article": "Art. 84"},
    {"test_id": "TC-014", "query": "Hours worked principles and waiting time compensability", "expected_article": "Art. 84"},
    {"test_id": "TC-015", "query": "Panggabi ang pasok ko pero walang additional 10 percent differential sa payroll", "expected_article": "Art. 86"},

    # --- DOMAIN 2: REST DAYS, HOLIDAYS & LEAVES ---
    {"test_id": "TC-016", "query": "Ilang araw na pahinga ang dapat ibigay sa manggagawa bawat linggo?", "expected_article": "Art. 91"},
    {"test_id": "TC-017", "query": "Right of workers to weekly rest day after continuous work", "expected_article": "Art. 91"},
    {"test_id": "TC-018", "query": "Pinapasok ako sa araw ng aking day off magkano ang dagdag na sahod?", "expected_article": "Art. 93"},
    {"test_id": "TC-019", "query": "Rate of compensation for work performed on a scheduled rest day", "expected_article": "Art. 93"},
    {"test_id": "TC-020", "query": "Kailan pwedeng obligahin ng kumpanya ang empleyado na pumasok sa rest day?", "expected_article": "Art. 92"},
    {"test_id": "TC-021", "query": "Exceptions where employer can compel work on rest periods", "expected_article": "Art. 92"},
    {"test_id": "TC-022", "query": "May sahod pa rin ba kahit hindi pumasok sa regular holiday?", "expected_article": "Art. 94"},
    {"test_id": "TC-023", "query": "Right to holiday pay and compensation for working on regular holidays", "expected_article": "Art. 94"},
    {"test_id": "TC-024", "query": "Ilang araw ang service incentive leave bawat taon?", "expected_article": "Art. 95"},
    {"test_id": "TC-025", "query": "Who are entitled to 5 days yearly service incentive leave?", "expected_article": "Art. 95"},
    {"test_id": "TC-026", "query": "Maaari bang i-convert sa cash ang hindi nagamit na service incentive leave?", "expected_article": "Art. 95"},

    # --- DOMAIN 3: WAGES, TIMING, FORM, AND MINIMUM WAGES ---
    {"test_id": "TC-027", "query": "Ano ang legal definition ng wage o minimum wage sa pribadong sektor?", "expected_article": "Art. 97"},
    {"test_id": "TC-028", "query": "Regional minimum wage determination and regional wage board rates", "expected_article": "Art. 99"},
    {"test_id": "TC-029", "query": "Binabaan ng amo ko ang dati kong sahod legal ba ang pagbawas ng sahod?", "expected_article": "Art. 100"},
    {"test_id": "TC-030", "query": "Prohibition against elimination or diminution of employee benefits and wages", "expected_article": "Art. 100"},
    {"test_id": "TC-031", "query": "Pwede bang bayaran ang sweldo gamit ang gift checks o vouchers imbes na pera?", "expected_article": "Art. 102"},
    {"test_id": "TC-032", "query": "Forms of payment for wages and prohibition of promissory notes or tokens", "expected_article": "Art. 102"},
    {"test_id": "TC-033", "query": "Kailan dapat i-release ang sweldo kada buwan?", "expected_article": "Art. 103"},
    {"test_id": "TC-034", "query": "Frequency and legal time of payment for employee compensation", "expected_article": "Art. 103"},
    {"test_id": "TC-035", "query": "Pinapasahod kami sa loob ng bar o sugalan bawal ba iyon ayon sa batas?", "expected_article": "Art. 104"},
    {"test_id": "TC-036", "query": "Designated place of wage payment and prohibited locations", "expected_article": "Art. 104"},
    {"test_id": "TC-037", "query": "Kanino dapat direktang ibigay ang sahod ng nagtrabahong empleyado?", "expected_article": "Art. 105"},
    {"test_id": "TC-038", "query": "Direct payment of wages requirement and valid exceptions", "expected_article": "Art. 105"},

    # --- DOMAIN 4: CONTRACTING, AGENCY WORKERS & SUBCONTRACTING ---
    {"test_id": "TC-039", "query": "Hindi kami binayaran ng agency namin, pwede ba naming habulin ang principal client?", "expected_article": "Art. 106"},
    {"test_id": "TC-040", "query": "Solidary liability of principal and contractor for unpaid wages", "expected_article": "Art. 106"},
    {"test_id": "TC-041", "query": "Ano ang kaibahan ng lehitimong contractor sa ipinagbabawal na labor-only contracting?", "expected_article": "Art. 106"},
    {"test_id": "TC-042", "query": "Indirect employer responsibilities in subcontracting agreements", "expected_article": "Art. 107"},
    {"test_id": "TC-043", "query": "Pwede bang humingi ng bond ang principal sa contractor para sa sahod ng tao?", "expected_article": "Art. 108"},
    {"test_id": "TC-044", "query": "Unpaid wages liability across subcontractor network and joint liability", "expected_article": "Art. 109"},

    # --- DOMAIN 5: PROHIBITED WAGE DEDUCTIONS & WITHHOLDING ---
    {"test_id": "TC-045", "query": "Kinakaltasan ang sahod ko para sa insurance na hindi ko pinayagan legal ba?", "expected_article": "Art. 113"},
    {"test_id": "TC-046", "query": "Authorized deductions from employee wages and allowable limits", "expected_article": "Art. 113"},
    {"test_id": "TC-047", "query": "Pinagbabayad kami ng cash deposit para sa posibleng pagkasira ng gamit sa tindahan", "expected_article": "Art. 114"},
    {"test_id": "TC-048", "query": "Deposits for loss or damage to equipment and tools regulations", "expected_article": "Art. 114"},
    {"test_id": "TC-049", "query": "Kailan pwedeng kaltasan ng employer ang empleyado sa nasirang kagamitan?", "expected_article": "Art. 115"},
    {"test_id": "TC-050", "query": "Limitations and due process before deductions for damaged tools", "expected_article": "Art. 115"},
    {"test_id": "TC-051", "query": "Iginigipit at ayaw ibigay ng amo ang sweldo ko para pilitin akong huwag umalis", "expected_article": "Art. 116"},
    {"test_id": "TC-052", "query": "Prohibition against withholding of wages and kickbacks", "expected_article": "Art. 116"},
    {"test_id": "TC-053", "query": "Pinipilit kami ng boss na bumili sa canteen niya bawas sa sweldo", "expected_article": "Art. 112"},
    {"test_id": "TC-054", "query": "Non-interference in wage disposal and purchasing freedom", "expected_article": "Art. 112"},

    # --- DOMAIN 6: WOMEN WORKERS, MATERNITY & DISCRIMINATION ---
    {"test_id": "TC-055", "query": "May hiwalay ba dapat na palikuran at upuan para sa kababaihan sa pabrika?", "expected_article": "Art. 131"},
    {"test_id": "TC-056", "query": "Facilities for women workers including seats and separate dressing rooms", "expected_article": "Art. 131"},
    {"test_id": "TC-057", "query": "Mas mababa ang sweldo ko kumpara sa lalaking pareho ang trabaho diskriminasyon ba ito?", "expected_article": "Art. 135"},
    {"test_id": "TC-058", "query": "Prohibition of wage discrimination on account of sex or gender", "expected_article": "Art. 135"},
    {"test_id": "TC-059", "query": "May clause sa kontrata ko na bawal mag-asawa habang nagtatrabaho may bisa ba ito?", "expected_article": "Art. 136"},
    {"test_id": "TC-060", "query": "Stipulation against marriage as a condition of employment validity", "expected_article": "Art. 136"},
    {"test_id": "TC-061", "query": "Tinanggal ako sa trabaho dahil nalaman ng amo na nabuntis ako", "expected_article": "Art. 137"},
    {"test_id": "TC-062", "query": "Prohibited acts against pregnant women workers and unlawful dismissal", "expected_article": "Art. 137"},
    {"test_id": "TC-063", "query": "Ano ang benepisyo sa maternity leave para sa mga manggagawang nanganak?", "expected_article": "Art. 133"},
    {"test_id": "TC-064", "query": "Maternity leave benefits and pregnancy leaves under Philippine labor law", "expected_article": "Art. 133"},

    # --- DOMAIN 7: MINORS, CHILD LABOR & KASAMBAHAY ---
    {"test_id": "TC-065", "query": "Ilang taon ang legal minimum age bago makapagtrabaho sa Pilipinas?", "expected_article": "Art. 139"},
    {"test_id": "TC-066", "query": "Minimum employable age and conditions for youth employment", "expected_article": "Art. 139"},
    {"test_id": "TC-067", "query": "Bawal ba ang menor de edad sa mga delikado at hazardous na trabaho?", "expected_article": "Art. 139"},
    {"test_id": "TC-068", "query": "Sino-sino ang itinuturing na domestic helpers o kasambahay sa batas?", "expected_article": "Art. 141"},
    {"test_id": "TC-069", "query": "Coverage of domestic workers and household service employment", "expected_article": "Art. 141"},
    {"test_id": "TC-070", "query": "Magkano ang minimum wage ng katulong sa bahay ayon sa labor code?", "expected_article": "Art. 143"},
    {"test_id": "TC-071", "query": "Obligasyon ba ng amo na bigyan ng pagkakataon makapag-aral ang kasambahay?", "expected_article": "Art. 148"},
    {"test_id": "TC-072", "query": "Opportunity for education and training of househelpers", "expected_article": "Art. 148"},

    # --- DOMAIN 8: WORKPLACE SAFETY, INJURY & DISABILITY BENEFITS ---
    {"test_id": "TC-073", "query": "Obligado ba ang may-ari ng planta na maglagay ng safety gear at first aid?", "expected_article": "Art. 162"},
    {"test_id": "TC-074", "query": "Occupational safety and health standards and compliance duties of employers", "expected_article": "Art. 162"},
    {"test_id": "TC-075", "query": "Nasaktan ako habang nagtatrabaho covered ba ako ng state insurance fund?", "expected_article": "Art. 168"},
    {"test_id": "TC-076", "query": "Compulsory coverage of employees under the State Insurance Fund and ECC", "expected_article": "Art. 168"},
    {"test_id": "TC-077", "query": "Ano ang benepisyo kapag pansamantalang hindi makapagtrabaho dahil sa injury sa site?", "expected_article": "Art. 197"},
    {"test_id": "TC-078", "query": "Temporary total disability compensation benefits and duration", "expected_article": "Art. 197"},
    {"test_id": "TC-079", "query": "Naputulan ako ng braso sa makina ano ang compensation sa habambuhay na disability?", "expected_article": "Art. 198"},
    {"test_id": "TC-080", "query": "Permanent total disability lifetime income and benefits calculation", "expected_article": "Art. 198"},

    # --- DOMAIN 9: ENFORCEMENT, DOLE INSPECTION & LABOR ARBITER ---
    {"test_id": "TC-081", "query": "Pwede bang mag-inspect bigla ang mga taga-DOLE sa aming pabrika?", "expected_article": "Art. 128"},
    {"test_id": "TC-082", "query": "Visitorial and enforcement power of the Secretary of Labor and workplace inspections", "expected_article": "Art. 128"},
    {"test_id": "TC-083", "query": "Saan pwedeng magsampa ng reklamo para sa illegal dismissal at unpaid wages?", "expected_article": "Art. 224"},
    {"test_id": "TC-084", "query": "Jurisdiction of Labor Arbiters over money claims, termination, and damages", "expected_article": "Art. 224"},
    {"test_id": "TC-085", "query": "May kapangyarihan ba ang DOLE na magpalabas ng stop work order kapag delikado?", "expected_article": "Art. 128"},
    {"test_id": "TC-086", "query": "Recovery of wages and simple money claims before DOLE regional directors", "expected_article": "Art. 129"},

    # --- DOMAIN 10: SECURITY OF TENURE & EMPLOYMENT STATUS ---
    {"test_id": "TC-087", "query": "Pwede ba akong tanggalin sa trabaho nang walang dahilan at due process?", "expected_article": "Art. 294"},
    {"test_id": "TC-088", "query": "Security of tenure protections against unjust termination without cause", "expected_article": "Art. 294"},
    {"test_id": "TC-089", "query": "Ilang buwan ang legal na maximum period para sa probationary employment?", "expected_article": "Art. 296"},
    {"test_id": "TC-090", "query": "Probationary period rules and qualification for regular status after six months", "expected_article": "Art. 296"},
    {"test_id": "TC-091", "query": "Ano ang basehan para matawag na regular employee ang isang manggagawa?", "expected_article": "Art. 295"},

    # --- DOMAIN 11: TERMINATION BY EMPLOYER - JUST & AUTHORIZED CAUSES ---
    {"test_id": "TC-092", "query": "Ano ang mga just causes para tanggalin ng kumpanya ang empleyado?", "expected_article": "Art. 297"},
    {"test_id": "TC-093", "query": "Termination by employer for serious misconduct, gross neglect, or willful disobedience", "expected_article": "Art. 297"},
    {"test_id": "TC-094", "query": "Nagsara ang opisina dahil nalugi may separation pay ba ang retrenchment?", "expected_article": "Art. 298"},
    {"test_id": "TC-095", "query": "Closure of establishment, redundancy, retrenchment authorized causes and separation pay", "expected_article": "Art. 298"},
    {"test_id": "TC-096", "query": "Pinaalis ako ng amo dahil nagka-tuberculosis ako legal ba ang pagtanggal dahil sa sakit?", "expected_article": "Art. 299"},
    {"test_id": "TC-097", "query": "Disease as ground for termination and medical certification requirements", "expected_article": "Art. 299"},

    # --- DOMAIN 12: RESIGNATION, RETIREMENT & GOVERNMENT EXCLUSION ---
    {"test_id": "TC-098", "query": "Ilang araw na notice ang kailangan ibigay kapag magreresign ang empleyado?", "expected_article": "Art. 300"},
    {"test_id": "TC-099", "query": "Ano ang retirement age at computation ng retirement pay sa pribadong sektor?", "expected_article": "Art. 302"},
    {"test_id": "TC-100", "query": "Kawani ako ng gobyerno sakop ba kami ng Philippine Labor Code?", "expected_article": "Art. 82"}
]

def run_evaluation():
    # 1. Login to get your Super Admin ID
    print("Logging into local SHIELD backend...")
    login_data = json.dumps({"username": "admin", "password": "adminpassword"}).encode('utf-8')
    login_req = urllib.request.Request(
        "http://127.0.0.1:8000/api/login",
        data=login_data,
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(login_req) as response:
            user_data = json.loads(response.read().decode())
            admin_id = user_data["id"]
            print(f"Login successful! Admin ID: {admin_id}\n")
    except Exception as e:
        print(f"Login failed. Make sure your uvicorn server is running. Error: {e}")
        return

    # 2. Send the 100 Test Cases to the Metrics Evaluator
    print("Sending 100 test cases to BGE-M3 for evaluation... This may take a minute depending on your CPU.")
    payload = {"test_cases": BENCHMARK_TEST_CASES}
    eval_req = urllib.request.Request(
        f"http://127.0.0.1:8000/api/admin/metrics/evaluate?requester_id={admin_id}",
        data=json.dumps(payload).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(eval_req) as eval_response:
            results = json.loads(eval_response.read().decode())
            print("\n" + "="*50)
            print("🚀 BGE-M3 EVALUATION RESULTS")
            print("="*50)
            print(json.dumps(results.get("summary", {}), indent=4))
            print("="*50)
            print("Check your terminal for detailed metrics like Mean Reciprocal Rank (MRR) and Precision@K.")
    except Exception as e:
        print(f"Evaluation failed. Error: {e}")

if __name__ == "__main__":
    run_evaluation()