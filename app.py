from flask import Flask, render_template
import folium

app = Flask(__name__)

# ข้อมูลสถานที่ ทริป 1 วันในจังหวัดกำแพงเพชร
locations = [
    {
        "id": 1,
        "name": "Kamphaeng Phet Rajabhat University",
        "lat": 16.475363033646648,
        "lon": 99.51018859763796,
        "description": "เริ่มต้นทริปที่มหาวิทยาลัยราชภัฏกำแพงเพชร แหล่งรวมความรู้และจุดนัดพบที่ร่มรื่น กว้างขวาง เหมาะกับการเริ่มต้นวัน",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTcrq4LK71BxG4lmGLo9OyPV6McSN65aJwmhQrZQLgOoa13-eS3L5ms9hTK&s=10",
        "gmap_url": "https://www.google.com/maps/search/?api=1&query=16.475363,99.510188"
    },
    {
        "id": 2,
        "name": "Cha Jai Story",
        "lat": 16.458889522395918,
        "lon": 99.51823512114223,
        "description": "แวะพักจิบเครื่องดื่มเย็นๆ ที่ร้าน Cha Jai Story คาเฟ่บรรยากาศดีที่สายถ่ายรูปและสายคาเฟ่ไม่ควรพลาด",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlWSApkTert3OkB19aj9djF2KSkF7xpshatqRY8bP2mw&s",
        "gmap_url": "https://www.google.com/maps/search/?api=1&query=16.458889,99.518235"
    },
    {
        "id": 3,
        "name": "Wat Wang Yang",
        "lat": 16.445915492330133,
        "lon": 99.5211389653202,
        "description": "สักการะสิ่งศักดิ์สิทธิ์และชมความงามของวัดวังยาง สถานที่สงบจิตใจริมเส้นทาง",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRMCI3N9MEPACGgydO_5ZXv5BMVwg_C664Dsku0RlSYMQ&s=10",
        "gmap_url": "https://www.google.com/maps/search/?api=1&query=16.445915,99.521138"
    },
    {
        "id": 4,
        "name": "ร้านยำป๊ะ หลังม.กำแพงเพชร",
        "lat": 16.460300227405117,
        "lon": 99.51315134588684,
        "description": "เติมความแซ่บมื้อกลางวันกับร้านยำรสเด็ดขวัญใจนักศึกษา รสชาติจัดจ้านถึงเครื่อง",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSH3dA07yA9xN10knNC1-drNMWGFO-LAodCmVlzMyhFOA&s",
        "gmap_url": "https://www.google.com/maps/search/?api=1&query=16.460300,99.513151"
    },
    {
        "id": 5,
        "name": "หน้าหมี - NAA'MHEE",
        "lat": 16.46223457396035,
        "lon": 99.52028602181694,
        "description": "ปิดท้ายทริปด้วยของอร่อยและบรรยากาศชิลๆ ที่ร้านหน้าหมี จุดแฮงเอาท์ยอดฮิตในพื้นที่",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ37rIYXYGcqQDMLDdT8cr1bXlyoAKoNXmrmdlotFANtw&s=10",
        "gmap_url": "https://www.google.com/maps/search/?api=1&query=16.462234,99.520286"
    }
     
]

@app.route("/")
def index():
    # หาพิกัดกึ่งกลางเพื่อตั้งเป็น Center ของแผนที่
    center_lat = sum(loc["lat"] for loc in locations) / len(locations)
    center_lon = sum(loc["lon"] for loc in locations) / len(locations)
    
    # สร้างแผนที่ Folium
    m = folium.Map(location=[center_lat, center_lon], zoom_start=14, tiles="CartoDB positron")
    
    # เพิ่ม Marker สำหรับแต่ละสถานที่
    for loc in locations:
        folium.Marker(
            [loc["lat"], loc["lon"]],
            popup=f"<b>{loc['name']}</b>",
            tooltip=loc["name"],
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)
        
    # ลากเส้นเชื่อมจุด (PolyLine) เพื่อแสดงเป็นเส้นทางทริป
    route_points = [[loc["lat"], loc["lon"]] for loc in locations]
    folium.PolyLine(route_points, color="red", weight=2.5, opacity=0.8).add_to(m)
    
    # ดึง HTML ของแผนที่มาใช้งาน
    map_html = m._repr_html_()
    
    # สร้าง URL นำทางรวมทุกจุด (จุดแรก ถึง จุดสุดท้าย)
    all_coords = "/".join([f"{loc['lat']},{loc['lon']}" for loc in locations])
    explore_route_url = f"https://www.google.com/maps/dir/{all_coords}"
    
    return render_template("index.html", locations=locations, map_html=map_html, explore_route_url=explore_route_url)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5031)
