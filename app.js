/* ==========================================================================
   Sisaket Rajabhat University Campus Map - JavaScript Application (Landing Page + Admin)
   ========================================================================== */

// --- 1. Default Building Dataset Configuration ---


const BUILDINGS = [
  {
    "id": 1,
    "name": "วิทยาลัยกฎหมายและการปกครอง",
    "nameEn": "College of Law and Government",
    "category": "academic",
    "coords": [
      734,
      898
    ],
    "realCoords": [
      15.11762,
      104.3592
    ],
    "description": "วิทยาลัยกฎหมายและการปกครอง มุ่งผลิตบัณฑิตทางด้านนิติศาสตร์ รัฐศาสตร์ และรัฐประศาสนศาสตร์ เพื่อตอบสนองการพัฒนาท้องถิ่นและประเทศชาติ",
    "phone": "045-643-600 ต่อ 2100",
    "tags": [
      "วกป",
      "กฎหมาย",
      "ปกครอง",
      "law",
      "government",
      "1"
    ]
  },
  {
    "id": 2,
    "name": "สำนักวิทยบริการและเทคโนโลยีสารสนเทศ (ห้องสมุด)",
    "nameEn": "Academic Resource and Information Technology Center (Library)",
    "category": "library",
    "coords": [
      782,
      1140
    ],
    "realCoords": [
      15.11795,
      104.3607
    ],
    "description": "ศูนย์กลางการเรียนรู้และให้บริการห้องสมุด เทคโนโลยีสารสนเทศ แก่นักศึกษา คณาจารย์ และบุคคลภายนอก มีพื้นที่อ่านหนังสือ ค้นคว้า และบริการคอมพิวเตอร์อินเทอร์เน็ต",
    "phone": "045-643-600 ต่อ 1500",
    "tags": [
      "วิทยบริการ",
      "ห้องสมุด",
      "หอสมุด",
      "library",
      "arit",
      "it",
      "สมุด",
      "2"
    ]
  },
  {
    "id": 3,
    "name": "อาคารศูนย์คอมพิวเตอร์",
    "nameEn": "Computer Center Building",
    "category": "library",
    "coords": [
      708,
      1090
    ],
    "realCoords": [
      15.11745,
      104.36045
    ],
    "description": "อาคารปฏิบัติการทางคอมพิวเตอร์และห้องเรียนคอมพิวเตอร์กลาง สำหรับวิชาเรียนทั่วไปและเป็นศูนย์แม่ข่ายระบบเครือข่ายอินเทอร์เน็ตของมหาวิทยาลัย",
    "phone": "045-643-600 ต่อ 1600",
    "tags": [
      "ศูนย์คอม",
      "คอมพิวเตอร์",
      "computer",
      "com",
      "คอม",
      "3"
    ]
  },
  {
    "id": 4,
    "name": "คณะศิลปศาสตร์และวิทยาศาสตร์",
    "nameEn": "Faculty of Liberal Arts and Science",
    "category": "academic",
    "coords": [
      826,
      976
    ],
    "realCoords": [
      15.11825,
      104.36005
    ],
    "description": "สำนักงานคณบดีและห้องเรียนหลักของคณะศิลปศาสตร์และวิทยาศาสตร์ รวมถึงสาขาวิชาทางด้านวิทยาศาสตร์บริสุทธิ์และศิลปศาสตร์",
    "phone": "045-643-600 ต่อ 2000",
    "tags": [
      "ศศว",
      "ศิลปศาสตร์",
      "วิทยาศาสตร์",
      "las",
      "sci",
      "science",
      "วศ",
      "4"
    ]
  },
  {
    "id": 5,
    "name": "คณะครุศาสตร์",
    "nameEn": "Faculty of Education",
    "category": "academic",
    "coords": [
      833,
      1208
    ],
    "realCoords": [
      15.11865,
      104.36115
    ],
    "description": "คณะวิชาผลิตครูและนักการศึกษาชั้นนำของจังหวัดศรีสะเกษ ผลิตบัณฑิตวิชาชีพครูในหลากหลายสาขาวิชา",
    "phone": "045-643-600 ต่อ 2300",
    "tags": [
      "ครุ",
      "ครุศาสตร์",
      "ศึกษาศาสตร์",
      "edu",
      "education",
      "ครู",
      "5"
    ]
  },
  {
    "id": 6,
    "name": "โรงเรียนสาธิตมหาวิทยาลัยราชภัฏศรีสะเกษ",
    "nameEn": "Demonstration School of SSKRU",
    "category": "academic",
    "coords": [
      768,
      1286
    ],
    "realCoords": [
      15.11805,
      104.36155
    ],
    "description": "โรงเรียนระดับปฐมวัยและประถมศึกษาสำหรับการทดลองสอน วิจัยหลักสูตร และจัดการศึกษาสาธิตที่มีคุณภาพให้แก่ชุมชน",
    "phone": "045-643-600 ต่อ 2400",
    "tags": [
      "สาธิต",
      "โรงเรียนสาธิต",
      "satit",
      "school",
      "6"
    ]
  },
  {
    "id": 7,
    "name": "คณะมนุษยศาสตร์และสังคมศาสตร์",
    "nameEn": "Faculty of Humanities and Social Sciences",
    "category": "academic",
    "coords": [
      917,
      1091
    ],
    "realCoords": [
      15.11895,
      104.36055
    ],
    "description": "อาคารเรียนคณะมนุษยศาสตร์และสังคมศาสตร์ จัดการศึกษาทางด้านภาษาประยุกต์ การพัฒนาชุมชน รัฐศาสตร์ ศิลปกรรมศาสตร์ และดนตรี",
    "phone": "045-643-600 ต่อ 2200",
    "tags": [
      "มนุษยศาสตร์",
      "สังคมศาสตร์",
      "huso",
      "humanities",
      "7"
    ]
  },
  {
    "id": 8,
    "name": "คณะบริหารธุรกิจและการบัญชี",
    "nameEn": "Faculty of Business Administration and Accounting",
    "category": "academic",
    "coords": [
      924,
      986
    ],
    "realCoords": [
      15.11925,
      104.35985
    ],
    "description": "อาคารเรียน คณะบริหารธุรกิจและการบัญชี จัดการศึกษาสาขาการบัญชี การจัดการ การตลาด คอมพิวเตอร์ธุรกิจ และการท่องเที่ยวการโรงแรม",
    "phone": "045-643-600 ต่อ 2500",
    "tags": [
      "บริหาร",
      "บัญชี",
      "จัดการ",
      "business",
      "mba",
      "accounting",
      "บธ",
      "8"
    ]
  },
  {
    "id": 9,
    "name": "สำนักงานอธิการบดีและบริหารกลาง",
    "nameEn": "Office of the President",
    "category": "office",
    "coords": [
      663,
      1236
    ],
    "realCoords": [
      15.11702,
      104.36118
    ],
    "description": "อาคารศูนย์กลางการบริหารงานราชการของมหาวิทยาลัย ที่ตั้งของสำนักแผนงาน กองคลัง กองกลาง กองนโยบาย และผู้บริหารระดับสูง",
    "phone": "045-643-600 ต่อ 1000",
    "tags": [
      "อธิการ",
      "อธิการบดี",
      "สำนักงานอธิการบดี",
      "op",
      "president",
      "ตึกอำนวยการ",
      "9"
    ]
  },
  {
    "id": 10,
    "name": "คณะพยาบาลศาสตร์",
    "nameEn": "Faculty of Nursing",
    "category": "academic",
    "coords": [
      812,
      734
    ],
    "realCoords": [
      15.11845,
      104.35725
    ],
    "description": "อาคารปฏิบัติการทางพยาบาลศาสตร์และสำนักงานคณะพยาบาลศาสตร์ มุ่งผลิตพยาบาลวิชาชีพที่มีทักษะเด่นด้านการดูแลสุขภาพชุมชน",
    "phone": "045-643-600 ต่อ 2600",
    "tags": [
      "พยาบาล",
      "พยาบาลศาสตร์",
      "nurse",
      "nursing",
      "10"
    ]
  },
  {
    "id": 11,
    "name": "ศูนย์ฝึกเทคโนโลยีดิจิทัล",
    "nameEn": "Digital Technology Training Center",
    "category": "facility",
    "coords": [
      533,
      772
    ],
    "realCoords": [
      15.11595,
      104.3579
    ],
    "description": "อาคารศูนย์ฝึกอบรม พัฒนาทักษะวิชาชีพ และให้บริการจัดประชุม สัมมนา อบรมทางคอมพิวเตอร์และเทคโนโลยีสารสนเทศแก่หน่วยงานภายในและภายนอก",
    "phone": "045-643-600 ต่อ 1800",
    "tags": [
      "ศูนย์ฝึก",
      "เทคโนโลยี",
      "ฝึกงาน",
      "ttc",
      "training",
      "11",
      "ดิจิทัล"
    ]
  },
  {
    "id": 12,
    "name": "โรงจอดรถบุคลากร",
    "nameEn": "Staff Parking Garage",
    "category": "other",
    "coords": [
      814,
      885
    ],
    "realCoords": [
      15.1179,
      104.35825
    ],
    "description": "อาคารที่จอดรถขนาดใหญ่สำหรับคณาจารย์และบุคลากรทางวิชาการ มหาวิทยาลัยราชภัฏศรีสะเกษ",
    "phone": "",
    "tags": [
      "จอดรถ",
      "โรงรถ",
      "โรงจอดรถ",
      "parking",
      "garage",
      "12"
    ]
  },
  {
    "id": 13,
    "name": "อาคารวิจัยและพัฒนาเทคโนโลยีอาหาร (Food technology)",
    "nameEn": "Food Technology Building",
    "category": "academic",
    "coords": [
      847,
      937
    ],
    "realCoords": [
      15.11835,
      104.35885
    ],
    "description": "อาคารวิจัย ผลิต และตรวจสอบความปลอดภัยด้านอาหารของคณะวิทยาศาสตร์ ตลอดจนเป็นศูนย์วิจัยด้านการเพิ่มมูลค่าผลิตภัณฑ์เกษตรแปรรูป",
    "phone": "045-643-600 ต่อ 2012",
    "tags": [
      "อาหาร",
      "ฟู้ดเทค",
      "food",
      "13"
    ]
  },
  {
    "id": 14,
    "name": "ศูนย์ศิลปวัฒนธรรม",
    "nameEn": "Art and Culture Center",
    "category": "facility",
    "coords": [
      582,
      892
    ],
    "realCoords": [
      15.11698,
      104.35895
    ],
    "description": "สถานที่เก็บรวบรวม จัดแสดง นิทรรศการด้านศิลปะโบราณคดีและวัฒนธรรมอีสานใต้ เพื่อการอนุรักษ์ ทำนุบำรุง และสืบสานมรดกทางวัฒนธรรม",
    "phone": "045-643-600 ต่อ 1200",
    "tags": [
      "ศิลปะ",
      "วัฒนธรรม",
      "ศูนย์ศิลป์",
      "culture",
      "art",
      "14"
    ]
  },
  {
    "id": 15,
    "name": "ศาลพระภูมิประจำมหาวิทยาลัย",
    "nameEn": "Shrine of the University",
    "category": "facility",
    "coords": [
      531,
      992
    ],
    "realCoords": [
      15.11695,
      104.35998
    ],
    "description": "ศาลพระภูมิเจ้าที่สิ่งศักดิ์สิทธิ์ประจำมหาวิทยาลัยราชภัฏศรีสะเกษ เป็นศูนย์รวมจิตใจของบุคลากรและนักศึกษา",
    "phone": "",
    "tags": [
      "พระ",
      "ศาลพระ",
      "shrine",
      "15"
    ]
  },
  {
    "id": 16,
    "name": "หอประชุมทีปังกรรัศมีโชติ",
    "nameEn": "Dipangkorn Rasmijoti Convention Hall",
    "category": "facility",
    "coords": [
      644,
      668
    ],
    "realCoords": [
      15.1169,
      104.35685
    ],
    "description": "หอประชุมอเนกประสงค์ขนาดใหญ่สำหรับใช้จัดพิธีพระราชทานปริญญาบัตร จัดงานสัมมนาขนาดใหญ่ กิจกรรมทางวิชาการ คอนเสิร์ต และการประชุมสำคัญระดับภูมิภาค",
    "phone": "045-643-600 ต่อ 1100",
    "tags": [
      "หอประชุม",
      "ทีปังกร",
      "ทีปังกรรัศมีโชติ",
      "hall",
      "convention",
      "16"
    ]
  },
  {
    "id": 17,
    "name": "โรงแรมศรีพฤทธาลัย ราชภัฏสัมมนาคาร",
    "nameEn": "Sriphrutthalai Rajabhat Hotel",
    "category": "other",
    "coords": [
      245,
      828
    ],
    "realCoords": [
      15.11425,
      104.3589
    ],
    "description": "โรงแรมและศูนย์จัดสัมมนาสัมมนาคาร ให้บริการห้องพัก ห้องจัดเลี้ยง และสระว่ายน้ำ ภายใต้การดูแลของมหาวิทยาลัย",
    "phone": "045-603-010",
    "tags": [
      "โรงแรม",
      "ศรีพฤทธาลัย",
      "สัมมนา",
      "hotel",
      "seminar",
      "ฟิตเนส",
      "17"
    ]
  },
  {
    "id": 18,
    "name": "อาคารวิทยาศาสตร์การกีฬา",
    "nameEn": "Sports Science Building",
    "category": "facility",
    "coords": [
      164,
      580
    ],
    "realCoords": [
      15.11495,
      104.35755
    ],
    "description": "อาคารวิทยาศาสตร์การกีฬา มีฟิตเนสเซ็นเตอร์ โรงยิม และสนามบาสเกตบอลในร่มสำหรับกิจกรรมพัฒนานักศึกษา",
    "phone": "045-643-600 ต่อ 1900",
    "tags": [
      "กีฬา",
      "ยิม",
      "สนาม",
      "sports",
      "gym",
      "stadium",
      "18"
    ]
  },
  {
    "id": 19,
    "name": "ศาลาพระพุทธรูป",
    "nameEn": "Buddha Image Pavilion",
    "category": "facility",
    "coords": [
      542,
      1039
    ],
    "realCoords": [
      15.11695,
      104.35998
    ],
    "description": "ศาลาที่ประดิษฐานพระพุทธรูปสิ่งศักดิ์สิทธิ์ประจำมหาวิทยาลัย เป็นที่เคารพสักการะของบุคลากรและผู้มาเยือน",
    "phone": "",
    "tags": [
      "พระ",
      "พระพุทธรูป",
      "buddha",
      "19"
    ]
  },
  {
    "id": 20,
    "name": "สนามมวย",
    "nameEn": "Tennis Courts",
    "category": "facility",
    "coords": [
      607,
      491
    ],
    "realCoords": [
      15.1186,
      104.3565
    ],
    "description": "สนามเทนนิสกลางแจ้งสำหรับการเรียนการสอน การแข่งขันและการออกกำลังกายของบุคลากรและนักศึกษา",
    "phone": "",
    "tags": [
      "20",
      "สนามมวย",
      "tennis courts"
    ]
  },
  {
    "id": 21,
    "name": "ร้านสะดวกซื้อ Mini Big C",
    "nameEn": "Mini Big C Convenience Store",
    "category": "other",
    "coords": [
      622,
      810
    ],
    "realCoords": [
      15.1172,
      104.3582
    ],
    "description": "ร้านสะดวกซื้อ มินิ บิ๊กซี สาขาภายในมหาวิทยาลัยราชภัฏศรีสะเกษ ให้บริการอาหาร เครื่องดื่ม และของใช้จำเป็นตลอด 24 ชั่วโมง",
    "phone": "",
    "tags": [
      "บิ๊กซี",
      "bigc",
      "c",
      "มินิบิ๊กซี",
      "ร้านสะดวกซื้อ",
      "21"
    ]
  }
];

// Network default connections (for Dijkstra pathfinder routing)
const DEFAULT_CONNECTIONS = [
  [1, 12], [1, 14], [1, 4], [1, 21],
  [2, 3], [2, 4], [2, 5],
  [3, 15],
  [5, 6], [5, 7],
  [6, 9],
  [7, 8],
  [8, 4], [8, 10], [8, 13],
  [9, 15], [9, 17],
  [10, 12], [10, 20],
  [11, 12], [11, 14], [11, 16], [11, 18], [11, 21],
  [12, 13],
  [14, 15], [14, 19],
  [15, 17],
  [16, 18], [16, 20],
  [17, 18], [17, 19],
  [18, 19]
];

const GEOFENCE = {
  latMin: 15.111500,
  latMax: 15.127500,
  lngMin: 104.353000,
  lngMax: 104.365000
};

// --- 2. Linear Calibration Equations (Convention Hall / Education Center) ---
const LAT1 = 15.116900, LNG1 = 104.356850;
const Y1 = 252, X1 = 472;

const LAT2 = 15.118650, LNG2 = 104.361150;
const Y2 = 772, X2 = 942;

const KY = (Y2 - Y1) / (LAT2 - LAT1);
const KX = (X2 - X1) / (LNG2 - LNG1);

function gpsToMap(lat, lng) {
  const y = Y1 + KY * (lat - LAT1);
  const x = X1 + KX * (lng - LNG1);
  return [y, x];
}

// --- 3. App State & Dynamic Storage ---
const IMAGE_BOUNDS = [[0, 0], [1024, 1536]];
const IMAGE_CENTER = [512, 768];
const pathGraph = {};

let map = null;
let markers = [];
let routePolyline = null;
let selectedBuilding = null;
let userPixelCoords = null;
let userMarker = null;
let activeFilters = 'all';

// Active Navigation & Event Tracking States
let activeTravelMode = 'walk'; // 'walk', 'bike', 'motorcycle', 'car'
let currentRouteCoords = [];   // Array of [y, x]
let navAnimMarker = null;
let navAnimId = null;
let isNavActive = false;
let navProgress = 0;
let targetBuildingName = "";

const TRAVEL_MODES = {
  walk:       { mps: 1.2, icon: 'fa-person-walking', label: 'เดินเท้า' },
  bike:       { mps: 3.5, icon: 'fa-bicycle', label: 'จักรยาน' },
  motorcycle: { mps: 7.5, icon: 'fa-motorcycle', label: 'มอเตอร์ไซค์' },
  car:        { mps: 6.0, icon: 'fa-car', label: 'รถยนต์' }
};

// User Session ID for Visitor Tracking
function getSessionId() {
  let sid = sessionStorage.getItem('sskru_session_id');
  if (!sid) {
    sid = 's_' + Math.random().toString(36).substring(2, 11) + '_' + Date.now();
    sessionStorage.setItem('sskru_session_id', sid);
  }
  return sid;
}

// Track user event to analytics API
function trackEvent(eventType, eventData = '') {
  try {
    fetch('/api/track', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        type: eventType,
        data: eventData,
        session_id: getSessionId(),
        path: window.location.pathname,
        referrer: document.referrer
      })
    }).catch(() => {});
  } catch (e) {}
}

let adminBuildings = [];

/* ==========================================================================
   Initialization Modules
   ========================================================================== */
document.addEventListener("DOMContentLoaded", () => {
  initMap();
  setupEventListeners();
  updateRealTimeStatus();
  loadBuildingsData();
  trackEvent('page_view', 'SSKRU Campus Map Loaded');

  setInterval(updateRealTimeStatus, 30000);
});

// Load dataset (attempts to fetch from backend REST API first, then falls back to LocalStorage)
async function loadBuildingsData() {
  try {
    const response = await fetch('/api/buildings');
    if (response.ok) {
      const json = await response.json();
      if (json.success && Array.isArray(json.data) && json.data.length > 0) {
        adminBuildings = json.data;
        isServerConnected = true;
        updateServerStatusPill(true);
        console.log("Loaded building data from Backend REST API.");
      } else {
        throw new Error("Invalid API format");
      }
    } else {
      throw new Error("HTTP " + response.status);
    }
  } catch (err) {
    console.warn("Backend REST API offline, falling back to LocalStorage / Default dataset.", err);
    isServerConnected = false;
    updateServerStatusPill(false);
    const localData = localStorage.getItem("sskru_buildings");
    if (localData) {
      try {
        adminBuildings = JSON.parse(localData);
      } catch (e) {
        adminBuildings = [...BUILDINGS];
      }
    } else {
      adminBuildings = [...BUILDINGS];
    }
  }

  // Refresh UI after data load
  buildNetworkGraph();
  renderBuildingCarousel(adminBuildings);
  populateDropdownSelectors();
  renderMarkers();
}

function updateServerStatusPill(online) {
  const pill = document.getElementById("admin-server-status-pill");
  const txt = document.getElementById("server-status-text");
  if (!pill || !txt) return;
  if (online) {
    pill.className = "admin-server-status";
    txt.innerHTML = '<i class="fa-solid fa-circle-check" style="color:#10b981;"></i> หลังบ้านออนไลน์ (Django API)';
  } else {
    pill.className = "admin-server-status offline";
    txt.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> ออฟไลน์ (LocalStorage)';
  }
}

function initMap() {
  map = L.map("map", {
    crs: L.CRS.Simple,
    minZoom: -2,
    maxZoom: 3,
    zoomControl: false,
    attributionControl: false,
    maxBounds: [[-250, -250], [1274, 1786]],
    maxBoundsViscosity: 0.8
  });

  L.imageOverlay("images/Map.png", IMAGE_BOUNDS).addTo(map);
  map.fitBounds(IMAGE_BOUNDS, { padding: [15, 15] });
  renderMarkers();
}

// --- 4. Campus Road Network Waypoints (Strictly follow campus asphalt roads!) ---
const ROAD_WAYPOINTS = {
  "R_ROUNDABOUT":        [700, 1180], // Main Campus Roundabout
  "R_EAST_GATE":         [700, 1340], // East Entrance Road
  "R_SATIT_ROAD":        [765, 1240], // Road in front of Satit School & Education
  "R_ADMIN_ROAD":        [670, 1210], // Road in front of Administration Building
  
  "R_CENTER_CROSS":      [700, 1080], // Central Crossroads near Computer Center & Library
  "R_SHRINE_ROAD":       [540, 1010], // Shrine & Buddha Pavilion Road
  "R_HUMANITIES_ROAD":   [900, 1090], // Road in front of Humanities Faculty
  
  "R_SOUTH_CROSS":       [780, 980],  // Crossroads near Liberal Arts & Business Faculty
  "R_BUSINESS_ROAD":     [920, 980],  // Road in front of Business Faculty
  "R_FOOD_TECH_ROAD":     [840, 920],  // Food Tech access road
  "R_LAW_ROAD":          [740, 900],  // Road in front of College of Law
  
  "R_WEST_CROSS_1":      [780, 845],  // Junction near Personnel Parking & Nursing Faculty
  "R_NURSING_ROAD":      [810, 750],  // Road in front of Nursing Faculty
  "R_WEST_CROSS_2":      [630, 800],  // Junction near Mini Big C & Cultural Center
  "R_CULTURAL_ROAD":     [585, 870],  // Road in front of Cultural Center
  
  "R_SPORTS_JUNCTION":   [630, 700],  // Junction near Convention Hall & Sports Complex
  "R_CONVENTION_ROAD":   [640, 680],  // Road in front of Convention Hall (ทีปังกร)
  "R_DIGITAL_CENTER_ROAD": [540, 770], // Road in front of Digital Training Center
  "R_BOXING_ROAD":       [607, 520],  // Sports & Boxing Ring road
  
  "R_NORTH_ROAD_1":      [450, 770],  // Main North Road going up to dorms
  "R_NORTH_ROAD_2":      [280, 780],  // Road in front of Sri Phrutthalai Hotel
  "R_NORTH_ROAD_3":      [200, 620]   // Road in front of Sports Science Stadium
};

const BUILDING_ROAD_ACCESS = {
  1:  "R_LAW_ROAD",
  2:  "R_CENTER_CROSS",
  3:  "R_CENTER_CROSS",
  4:  "R_SOUTH_CROSS",
  5:  "R_SATIT_ROAD",
  6:  "R_SATIT_ROAD",
  7:  "R_HUMANITIES_ROAD",
  8:  "R_BUSINESS_ROAD",
  9:  "R_ADMIN_ROAD",
  10: "R_NURSING_ROAD",
  11: "R_DIGITAL_CENTER_ROAD",
  12: "R_LAW_ROAD",
  13: "R_FOOD_TECH_ROAD",
  14: "R_CULTURAL_ROAD",
  15: "R_SHRINE_ROAD",
  16: "R_CONVENTION_ROAD",
  17: "R_NORTH_ROAD_2",
  18: "R_NORTH_ROAD_3",
  19: "R_SHRINE_ROAD",
  20: "R_BOXING_ROAD",
  21: "R_WEST_CROSS_2"
};

const ROAD_CONNECTIONS = [
  ["R_ROUNDABOUT", "R_EAST_GATE"],
  ["R_ROUNDABOUT", "R_ADMIN_ROAD"],
  ["R_ROUNDABOUT", "R_SATIT_ROAD"],
  ["R_ROUNDABOUT", "R_CENTER_CROSS"],
  
  ["R_SATIT_ROAD", "R_HUMANITIES_ROAD"],
  
  ["R_CENTER_CROSS", "R_SHRINE_ROAD"],
  ["R_CENTER_CROSS", "R_HUMANITIES_ROAD"],
  ["R_CENTER_CROSS", "R_SOUTH_CROSS"],
  ["R_CENTER_CROSS", "R_LAW_ROAD"],
  
  ["R_SOUTH_CROSS", "R_LAW_ROAD"],
  ["R_SOUTH_CROSS", "R_FOOD_TECH_ROAD"],
  ["R_SOUTH_CROSS", "R_BUSINESS_ROAD"],
  ["R_BUSINESS_ROAD", "R_HUMANITIES_ROAD"],
  
  ["R_LAW_ROAD", "R_WEST_CROSS_1"],
  ["R_WEST_CROSS_1", "R_NURSING_ROAD"],
  ["R_WEST_CROSS_1", "R_WEST_CROSS_2"],
  ["R_WEST_CROSS_1", "R_FOOD_TECH_ROAD"],
  
  ["R_WEST_CROSS_2", "R_CULTURAL_ROAD"],
  ["R_WEST_CROSS_2", "R_SPORTS_JUNCTION"],
  ["R_CULTURAL_ROAD", "R_DIGITAL_CENTER_ROAD"],
  
  ["R_SPORTS_JUNCTION", "R_CONVENTION_ROAD"],
  ["R_SPORTS_JUNCTION", "R_DIGITAL_CENTER_ROAD"],
  ["R_SPORTS_JUNCTION", "R_BOXING_ROAD"],
  ["R_SPORTS_JUNCTION", "R_NORTH_ROAD_1"],
  
  ["R_NORTH_ROAD_1", "R_NORTH_ROAD_2"],
  ["R_NORTH_ROAD_2", "R_NORTH_ROAD_3"]
];

function getNodeCoords(nodeId) {
  if (typeof nodeId === 'number' || (!isNaN(Number(nodeId)) && typeof nodeId !== 'symbol')) {
    const num = Number(nodeId);
    const b = adminBuildings.find(item => item.id === num);
    if (b) return b.coords;
  }
  if (ROAD_WAYPOINTS[nodeId]) {
    return ROAD_WAYPOINTS[nodeId];
  }
  return null;
}

function addEdgeToGraph(u, v) {
  const cU = getNodeCoords(u);
  const cV = getNodeCoords(v);
  if (cU && cV) {
    const dx = cU[1] - cV[1];
    const dy = cU[0] - cV[0];
    const dist = Math.sqrt(dx * dx + dy * dy);

    if (!pathGraph[u]) pathGraph[u] = {};
    if (!pathGraph[v]) pathGraph[v] = {};

    pathGraph[u][v] = dist;
    pathGraph[v][u] = dist;
  }
}

function buildNetworkGraph() {
  for (let id in pathGraph) delete pathGraph[id];

  // 1. Add buildings and connect each to its front road access node
  adminBuildings.forEach(b => {
    pathGraph[b.id] = {};
    const accessNode = BUILDING_ROAD_ACCESS[b.id] || "R_CENTER_CROSS";
    addEdgeToGraph(b.id, accessNode);
  });

  // 2. Add road waypoints
  for (let rId in ROAD_WAYPOINTS) {
    if (!pathGraph[rId]) pathGraph[rId] = {};
  }

  // 3. Connect road network segments
  ROAD_CONNECTIONS.forEach(([u, v]) => {
    addEdgeToGraph(u, v);
  });
}

/* ==========================================================================
   UI / Render Engines
   ========================================================================== */

function renderMarkers() {
  markers.forEach(m => map.removeLayer(m));
  markers = [];

  const filteredList = activeFilters === 'all'
    ? adminBuildings
    : adminBuildings.filter(b => b.category === activeFilters);

  filteredList.forEach(b => {
    const displayNum = b.id === 21 ? "C" : b.id;

    const customIcon = L.divIcon({
      html: `
        <div class="marker-pin-wrapper marker-${b.category}">
          <div class="marker-pin"></div>
          <span class="marker-number">${displayNum}</span>
        </div>
      `,
      className: "custom-leaflet-marker",
      iconSize: [32, 38],
      iconAnchor: [16, 38]
    });

    // Make draggable ONLY in Admin Mode
    const marker = L.marker(b.coords, {
      icon: customIcon,
      draggable: isAdminMode
    }).addTo(map);

    marker.bindTooltip(`<b>${displayNum}. ${b.name}</b>`, {
      direction: 'top',
      offset: [0, -40],
      opacity: 0.9
    });

    if (isAdminMode) {
      marker.on("dragend", (e) => {
        const newPos = marker.getLatLng();
        const y = Math.round(newPos.lat);
        const x = Math.round(newPos.lng);
        b.coords = [y, x];
        saveBuildingsToStorage();
        showToast(`ย้ายตึก ${displayNum} ไปยังพิกัด [Y: ${y}, X: ${x}] สำเร็จ`);

        // Feed coordinate form input if open
        if (document.getElementById("edit-building-id").value == b.id) {
          document.getElementById("edit-building-coords").value = `[${y}, ${x}]`;
        }
      });
    }

    marker.on("click", () => {
      if (isAdminMode) {
        openEditBuildingForm(b);
      } else {
        selectBuilding(b);
      }
    });

    markers.push(marker);
  });
}

function renderBuildingCarousel(list) {
  const container = document.getElementById("building-carousel-wrapper");
  const counter = document.getElementById("carousel-item-counter");
  container.innerHTML = "";

  if (counter) {
    counter.textContent = `${list.length} ตึกอาคาร`;
  }

  if (list.length === 0) {
    container.innerHTML = `
      <div class="loading-placeholder-carousel">
        <i class="fa-solid fa-folder-open fa-lg"></i> ไม่พบรายการอาคารในหมวดหมู่นี้
      </div>
    `;
    return;
  }

  list.forEach(b => {
    const status = getBuildingStatus(b);
    const displayNum = b.id === 21 ? "C" : b.id;

    const card = document.createElement("div");
    card.className = `carousel-card ${b.category}`;
    card.id = `b-card-${b.id}`;
    card.setAttribute("role", "listitem");
    card.setAttribute("tabindex", "0");

    card.innerHTML = `
      <div class="card-num-circle">${displayNum}</div>
      <div class="card-info">
        <div class="card-name">${b.name}</div>
        <div class="card-subname">${b.nameEn}</div>
        <div class="card-meta">
          <span class="card-category-lbl category-${b.category}">${translateCategory(b.category)}</span>
          <span class="status-dot-mini ${status.isOpen ? 'open' : 'closed'}"></span>
          <span style="font-size: 10px; color: var(--text-secondary);">${status.isOpen ? 'เปิดอยู่' : 'ปิดแล้ว'}</span>
        </div>
      </div>
    `;

    card.addEventListener("click", () => {
      if (isAdminMode) {
        openEditBuildingForm(b);
      } else {
        selectBuilding(b);
      }
    });
    card.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        if (isAdminMode) {
          openEditBuildingForm(b);
        } else {
          selectBuilding(b);
        }
      }
    });

    container.appendChild(card);
  });
}

function translateCategory(cat) {
  switch (cat) {
    case 'academic': return 'เรียน/คณะ';
    case 'office': return 'สำนักงาน';
    case 'facility': return 'บริการ';
    case 'library': return 'ไอที/สมุด';
    default: return 'อื่นๆ';
  }
}

function populateDropdownSelectors() {
  const sourceSel = document.getElementById("select-nav-source");
  const destSel = document.getElementById("select-nav-dest");

  sourceSel.innerHTML = `
    <option value="">-- เลือกสถานที่เริ่มต้น --</option>
    <option value="my_location">📍 ตำแหน่งปัจจุบันของคุณ (GPS)</option>
  `;
  destSel.innerHTML = '<option value="">-- เลือกสถานที่ปลายทาง --</option>';

  const sorted = [...adminBuildings].sort((a, b) => a.id - b.id);

  sorted.forEach(b => {
    const displayNum = b.id === 21 ? "C" : b.id;
    const optText = `${displayNum}. ${b.name}`;

    const optS = document.createElement("option");
    optS.value = b.id;
    optS.textContent = optText;
    sourceSel.appendChild(optS);

    const optD = document.createElement("option");
    optD.value = b.id;
    optD.textContent = optText;
    destSel.appendChild(optD);
  });
}

function updateRealTimeStatus() {
  adminBuildings.forEach(b => {
    const itemMeta = document.querySelector(`#b-card-${b.id} .status-dot-mini`);
    const itemText = document.querySelector(`#b-card-${b.id} .card-meta span:last-child`);
    if (itemMeta && itemText) {
      const status = getBuildingStatus(b);
      itemMeta.className = `status-dot-mini ${status.isOpen ? 'open' : 'closed'}`;
      itemText.textContent = status.isOpen ? 'เปิดอยู่' : 'ปิดแล้ว';
    }
  });

  if (selectedBuilding) {
    const status = getBuildingStatus(selectedBuilding);
    const badge = document.getElementById("panel-badge-status");
    const txt = document.getElementById("panel-status-text");
    const metaHours = document.getElementById("panel-meta-hours");

    if (badge && txt) {
      badge.className = `building-status-badge ${status.isOpen ? 'open' : 'closed'}`;
      txt.textContent = status.isOpen ? 'เปิดให้บริการ' : 'ปิดให้บริการ';
      metaHours.textContent = status.hoursText;
    }
  }
}

function getBuildingStatus(b) {
  const now = new Date();
  const day = now.getDay();
  const hours = now.getHours();
  const minutes = now.getMinutes();
  const currentMinutes = hours * 60 + minutes;

  let isOpen = false;
  let hoursText = "";

  if (b.id === 17 || b.id === 21) {
    isOpen = true;
    hoursText = "เปิดบริการทุกวัน ตลอด 24 ชั่วโมง";
  } else if (b.id === 2) {
    hoursText = "จันทร์ - ศุกร์: 08:30 - 20:00 น. | เสาร์ - อาทิตย์: 09:00 - 16:30 น.";
    if (day >= 1 && day <= 5) {
      if (currentMinutes >= 8 * 60 + 30 && currentMinutes <= 20 * 60) {
        isOpen = true;
      }
    } else {
      if (currentMinutes >= 9 * 60 && currentMinutes <= 16 * 60 + 30) {
        isOpen = true;
      }
    }
  } else if (b.id === 18) {
    hoursText = "เปิดบริการทุกวัน: 06:00 - 21:00 น.";
    if (currentMinutes >= 6 * 60 && currentMinutes <= 21 * 60) {
      isOpen = true;
    }
  } else if (b.id === 13) {
    hoursText = "จันทร์ - ศุกร์: 07:00 - 17:00 น. (ปิดวันเสาร์ - อาทิตย์)";
    if (day >= 1 && day <= 5) {
      if (currentMinutes >= 7 * 60 && currentMinutes <= 17 * 60) {
        isOpen = true;
      }
    }
  } else {
    hoursText = "จันทร์ - ศุกร์: 08:30 - 16:30 น. (ปิดวันเสาร์ - อาทิตย์)";
    if (day >= 1 && day <= 5) {
      if (currentMinutes >= 8 * 60 + 30 && currentMinutes <= 16 * 60 + 30) {
        isOpen = true;
      }
    }
  }

  return { isOpen, hoursText };
}

/* ==========================================================================
   Action & Selection Handlers
   ========================================================================== */

function selectBuilding(b) {
  selectedBuilding = b;
  trackEvent('building_select', b.name);
  const displayNum = b.id === 21 ? "C" : b.id;

  const card = document.getElementById(`b-card-${b.id}`);
  const wrapper = document.getElementById("building-carousel-wrapper");

  if (card && wrapper) {
    document.querySelectorAll(".carousel-card").forEach(el => el.classList.remove("selected"));
    card.classList.add("selected");

    const cardOffset = card.offsetLeft;
    const cardWidth = card.clientWidth;
    const wrapperWidth = wrapper.clientWidth;
    const scrollPos = cardOffset - (wrapperWidth / 2) + (cardWidth / 2);

    wrapper.scrollTo({
      left: scrollPos,
      behavior: "smooth"
    });
  }

  map.setView(b.coords, 1, { animate: true, duration: 0.6 });

  document.getElementById("panel-title-th").textContent = b.name;
  document.getElementById("panel-title-en").textContent = b.nameEn;
  document.getElementById("panel-description").textContent = b.description;
  document.getElementById("panel-meta-coords").textContent = `${b.realCoords[0].toFixed(6)}, ${b.realCoords[1].toFixed(6)}`;

  const badgeCat = document.getElementById("panel-badge-category");
  badgeCat.className = `building-cat-badge category-${b.category}`;
  badgeCat.textContent = translateCategory(b.category);

  const phoneRow = document.getElementById("panel-meta-phone-row");
  const phoneVal = document.getElementById("panel-meta-phone");
  const btnCall = document.getElementById("btn-action-call");

  if (b.phone) {
    phoneRow.style.display = "flex";
    phoneVal.textContent = b.phone;
    btnCall.style.display = "flex";
    btnCall.onclick = () => { window.location.href = `tel:${b.phone.replace(/[^0-9+]/g, '')}`; };
  } else {
    phoneRow.style.display = "none";
    btnCall.style.display = "none";
  }

  const imgContainer = document.getElementById("panel-image-container");
  imgContainer.innerHTML = "";

  const gradientDiv = document.createElement("div");
  gradientDiv.className = `info-panel-placeholder ${b.category}`;
  gradientDiv.innerHTML = `
    <i class="fa-solid fa-school fa-3x" style="margin-bottom: 12px; opacity: 0.85;"></i>
    <h3 style="font-size: 20px; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.25);">${displayNum}. ${b.name}</h3>
    <p style="font-size: 12px; opacity: 0.9; font-weight: 300;">วิทยาเขต มหาวิทยาลัยราชภัฏศรีสะเกษ</p>
  `;
  imgContainer.appendChild(gradientDiv);

  const status = getBuildingStatus(b);
  const badgeStatus = document.getElementById("panel-badge-status");
  const txtStatus = document.getElementById("panel-status-text");
  const txtHours = document.getElementById("panel-meta-hours");

  badgeStatus.className = `building-status-badge ${status.isOpen ? 'open' : 'closed'}`;
  txtStatus.textContent = status.isOpen ? 'เปิดให้บริการ' : 'ปิดให้บริการ';
  txtHours.textContent = status.hoursText;

  // Reset tabs to default
  document.querySelectorAll(".info-tab-btn").forEach(t => t.classList.remove("active"));
  document.querySelectorAll(".info-tab-pane").forEach(p => p.classList.remove("active"));
  const defaultTabBtn = document.querySelector('.info-tab-btn[data-tab="info"]');
  const defaultTabPane = document.getElementById("tab-info");
  if (defaultTabBtn) defaultTabBtn.classList.add("active");
  if (defaultTabPane) defaultTabPane.classList.add("active");

  document.getElementById("building-info-panel").classList.add("active");

  // Smart Navigation Button — opens in-app route, or external maps on mobile
  document.getElementById("btn-action-gmaps").onclick = () => {
    openSmartNavigation(b);
  };

  // Save Button
  document.getElementById("btn-action-save").onclick = () => {
    showToast(`📌 บันทึก "${b.name}" สำเร็จ (ฟีเจอร์บัญชีผู้ใช้)`);
  };

  document.getElementById("btn-action-share").onclick = () => {
    shareBuildingLocation(b);
  };
}

function closeInfoPanel() {
  document.getElementById("building-info-panel").classList.remove("active");
  document.querySelectorAll(".carousel-card").forEach(el => el.classList.remove("selected"));
  selectedBuilding = null;
}

function shareBuildingLocation(b) {
  const displayNum = b.id === 21 ? "C" : b.id;
  const shareTitle = `ตำแหน่ง ${b.name}`;
  const shareText = `เช็คพิกัดอาคาร ${displayNum}. ${b.name} (${b.nameEn}) ในวิทยาเขต มรภ.ศรีสะเกษ ได้ที่พิกัดด้านล่าง`;
  const shareUrl = `https://www.google.com/maps/search/?api=1&query=${b.realCoords[0]},${b.realCoords[1]}`;

  if (navigator.share) {
    navigator.share({
      title: shareTitle,
      text: shareText,
      url: shareUrl
    }).catch(console.error);
  } else {
    navigator.clipboard.writeText(`${shareText}\nลิงก์พิกัด: ${shareUrl}`).then(() => {
      showToast("คัดลอกลิงก์แชร์ลงคลิปบอร์ดแล้ว");
    }).catch(() => {
      showToast("ไม่สามารถแชร์ตำแหน่งได้");
    });
  }
}

function showToast(msg) {
  const toast = document.getElementById("toast-bar");
  document.getElementById("toast-message").textContent = msg;
  toast.classList.add("active");
  setTimeout(() => {
    toast.classList.remove("active");
  }, 3500);
}

function showModal(title, message, iconType = 'warning') {
  const modal = document.getElementById("custom-modal-overlay");
  const tText = document.getElementById("modal-title-text");
  const dText = document.getElementById("modal-desc-text");
  const icon = document.getElementById("modal-status-icon");

  tText.textContent = title;
  dText.textContent = message;

  icon.className = `modal-icon ${iconType}`;
  if (iconType === 'warning') {
    icon.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i>';
  } else if (iconType === 'success') {
    icon.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
  } else {
    icon.innerHTML = '<i class="fa-solid fa-circle-info"></i>';
  }

  modal.classList.add("active");
}

/* ==========================================================================
   Search & Filter Systems
   ========================================================================== */

function filterByCategory(category) {
  activeFilters = category;

  document.querySelectorAll(".category-tab").forEach(tab => {
    if (tab.getAttribute("data-category") === category) {
      tab.classList.add("active");
    } else {
      tab.classList.remove("active");
    }
  });

  const filtered = category === 'all'
    ? adminBuildings
    : adminBuildings.filter(b => b.category === category);

  renderBuildingCarousel(filtered);
  renderMarkers();
}

function handleSearchInput(e) {
  const query = e.target.value.trim().toLowerCase();
  const dropdown = document.getElementById("search-suggestions");
  const clearBtn = document.getElementById("btn-search-clear");

  if (!query) {
    dropdown.style.display = "none";
    clearBtn.style.display = "none";
    return;
  }

  clearBtn.style.display = "block";

  const matches = adminBuildings.filter(b => {
    return b.name.toLowerCase().includes(query) ||
      b.nameEn.toLowerCase().includes(query) ||
      b.id.toString() === query ||
      (b.id === 21 && query === "c") ||
      b.tags.some(t => t.toLowerCase().includes(query));
  });

  if (matches.length === 0) {
    dropdown.innerHTML = `
      <div style="padding: 15px; text-align: center; color: var(--text-secondary); font-size: 13px;">
        <i class="fa-solid fa-circle-question"></i> ไม่พบอาคารที่ค้นหา
      </div>
    `;
    dropdown.style.display = "block";
    return;
  }

  dropdown.innerHTML = "";
  matches.forEach(b => {
    const displayNum = b.id === 21 ? "C" : b.id;
    const item = document.createElement("div");
    item.className = "autocomplete-item";
    item.setAttribute("role", "option");

    item.innerHTML = `
      <div class="autocomplete-icon">${displayNum}</div>
      <div class="autocomplete-text">
        <div class="autocomplete-title">${b.name}</div>
        <div class="autocomplete-subtitle">${b.nameEn}</div>
      </div>
    `;

    item.onclick = () => {
      if (isAdminMode) {
        openEditBuildingForm(b);
      } else {
        selectBuilding(b);
      }
      dropdown.style.display = "none";
      e.target.value = b.name;
    };

    dropdown.appendChild(item);
  });

  dropdown.style.display = "block";
}

/* ==========================================================================
   GPS Tracking & Geofencing (Calibrated)
   ========================================================================== */

function trackUserLocation() {
  if (!navigator.geolocation) {
    showModal("ไม่รองรับ GPS", "อุปกรณ์ของคุณไม่รองรับบริการตรวจหาพิกัดตำแหน่งภูมิศาสตร์", "info");
    return;
  }

  navigator.geolocation.getCurrentPosition(
    (pos) => {
      const lat = pos.coords.latitude;
      const lng = pos.coords.longitude;

      if (lat >= GEOFENCE.latMin && lat <= GEOFENCE.latMax &&
        lng >= GEOFENCE.lngMin && lng <= GEOFENCE.lngMax) {

        userPixelCoords = gpsToMap(lat, lng);

        if (userMarker) {
          userMarker.setLatLng(userPixelCoords);
        } else {
          const userIcon = L.divIcon({
            html: '<div class="user-location-marker"></div>',
            className: 'custom-leaflet-marker',
            iconSize: [16, 16],
            iconAnchor: [8, 8]
          });
          userMarker = L.marker(userPixelCoords, { icon: userIcon }).addTo(map);
          userMarker.bindTooltip("ตำแหน่งปัจจุบันของฉัน");
        }

        map.setView(userPixelCoords, 1, { animate: true });
        showToast("ระบุพิกัด GPS บนแผนผังเรียบร้อย");
      } else {
        userPixelCoords = null;
        if (userMarker) {
          map.removeLayer(userMarker);
          userMarker = null;
        }
        showModal(
          "อยู่นอกพื้นที่การใช้งาน",
          `ระบบระบุตำแหน่งตรวจพบพิกัด (${lat.toFixed(6)}, ${lng.toFixed(6)}) ซึ่งอยู่นอกพื้นที่ มรภ.ศรีสะเกษ ระบบไม่สามารถแสดงตัวตนบนแผนผัง 3D ได้ แต่ท่านยังคงดูและค้นหาตึกได้ตามปกติ`,
          "warning"
        );
      }
    },
    (err) => {
      userPixelCoords = null;
      let errMsg = "ไม่สามารถเข้าถึงสิทธิ์ตำแหน่ง GPS ได้ กรุณาเปิดบริการตำแหน่งที่ตั้งบนเบราว์เซอร์";
      if (err.code === err.PERMISSION_DENIED) {
        errMsg = "สิทธิ์การเข้าถึงตำแหน่ง GPS ถูกปฏิเสธ กรุณาอนุญาตเข้าสิทธิ์พิกัดบนเบราว์เซอร์";
      }
      showModal("ระบุตำแหน่งพิกัดผิดพลาด", errMsg, "warning");
    },
    { enableHighAccuracy: true, timeout: 8000 }
  );
}

/* ==========================================================================
   Dijkstra Pathfinding Navigation Engine
   ========================================================================== */

function solveDijkstra(startId, endId) {
  const distances = {};
  const prev = {};
  const unvisited = new Set();

  for (let nodeId in pathGraph) {
    distances[nodeId] = Infinity;
    prev[nodeId] = null;
    unvisited.add(Number(nodeId));
  }

  distances[startId] = 0;

  while (unvisited.size > 0) {
    let current = null;
    let minDistance = Infinity;

    for (let nodeId of unvisited) {
      if (distances[nodeId] < minDistance) {
        minDistance = distances[nodeId];
        current = nodeId;
      }
    }

    if (current === null || current === endId) {
      break;
    }

    unvisited.delete(current);

    const neighbors = pathGraph[current];
    for (let neighborId in neighbors) {
      const neighbor = Number(neighborId);
      if (!unvisited.has(neighbor)) continue;

      const weight = neighbors[neighborId];
      const alt = distances[current] + weight;

      if (alt < distances[neighbor]) {
        distances[neighbor] = alt;
        prev[neighbor] = current;
      }
    }
  }

  const path = [];
  let u = endId;
  if (prev[u] !== null || u === startId) {
    while (u !== null) {
      path.unshift(u);
      u = prev[u];
    }
  }

  return {
    path: path,
    distance: distances[endId]
  };
}

/* ==========================================================================
   Real-Time Grab Rider Motion & Path Animation Engine
   ========================================================================== */

function createGrabRiderIcon(mode = 'grab', headingDeg = 0) {
  const modeInfo = TRAVEL_MODES[mode] || TRAVEL_MODES.grab;
  return L.divIcon({
    className: 'grab-leaflet-icon-wrapper',
    html: `
      <div class="grab-rider-marker-wrapper">
        <div class="grab-rider-pulse-ring"></div>
        <div class="grab-rider-avatar" style="transform: rotate(${Math.round(headingDeg)}deg);">
          <i class="fa-solid ${modeInfo.icon}"></i>
          <div class="grab-rider-heading-arrow"></div>
        </div>
      </div>
    `,
    iconSize: [48, 48],
    iconAnchor: [24, 24]
  });
}

function getInterpolatedPointAndAngle(coords, progress) {
  if (!coords || coords.length === 0) return { lat: 0, lng: 0, angle: 0 };
  if (coords.length === 1 || progress <= 0) return { lat: coords[0][0], lng: coords[0][1], angle: 0 };
  if (progress >= 1) {
    const last = coords[coords.length - 1];
    const prev = coords[coords.length - 2];
    const dy = last[0] - prev[0];
    const dx = last[1] - prev[1];
    const angle = (Math.atan2(dx, dy) * 180 / Math.PI);
    return { lat: last[0], lng: last[1], angle };
  }

  let totalLen = 0;
  const segLens = [];
  for (let i = 0; i < coords.length - 1; i++) {
    const dy = coords[i+1][0] - coords[i][0];
    const dx = coords[i+1][1] - coords[i][1];
    const len = Math.sqrt(dx * dx + dy * dy);
    segLens.push(len);
    totalLen += len;
  }

  const targetDist = progress * totalLen;
  let accumulated = 0;

  for (let i = 0; i < segLens.length; i++) {
    const segLen = segLens[i];
    if (accumulated + segLen >= targetDist || i === segLens.length - 1) {
      const segT = segLen > 0 ? (targetDist - accumulated) / segLen : 0;
      const lat = coords[i][0] + segT * (coords[i+1][0] - coords[i][0]);
      const lng = coords[i][1] + segT * (coords[i+1][1] - coords[i][1]);

      const dy = coords[i+1][0] - coords[i][0];
      const dx = coords[i+1][1] - coords[i][1];
      const angle = (Math.atan2(dx, dy) * 180 / Math.PI);

      return { lat, lng, angle };
    }
    accumulated += segLen;
  }

  const endPt = coords[coords.length - 1];
  return { lat: endPt[0], lng: endPt[1], angle: 0 };
}

function updateGrabMotionUI() {
  const pct = Math.round(grabProgress * 100);
  const fill = document.getElementById("grab-progress-fill");
  const text = document.getElementById("grab-progress-text");
  const title = document.getElementById("grab-motion-status-title");
  const playLbl = document.getElementById("lbl-grab-play");
  const playIcon = document.getElementById("icon-grab-play");

  if (fill) fill.style.width = `${pct}%`;
  if (text) text.textContent = `${pct}%`;

  if (isGrabAnimating) {
    if (playLbl) playLbl.textContent = "หยุดชั่วคราว";
    if (playIcon) playIcon.className = "fa-solid fa-pause";
    if (title) title.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> กำลังนำทางไป ${targetBuildingName || 'จุดหมาย'}...`;
  } else {
    if (playLbl) playLbl.textContent = grabProgress >= 1 ? "เล่นอีกครั้ง" : "เริ่มเคลื่อนที่";
    if (playIcon) playIcon.className = grabProgress >= 1 ? "fa-solid fa-rotate-left" : "fa-solid fa-play";
    if (title) {
      title.textContent = grabProgress >= 1 ? "🎉 ถึงจุดหมายปลายทางแล้ว!" : "ระบบนำทาง Grab Rider พร้อมลุย";
    }
  }
}

function startGrabRiderMotion() {
  if (currentRouteCoords.length < 2) return;

  if (grabProgress >= 1) {
    grabProgress = 0;
  }

  isGrabAnimating = true;
  updateGrabMotionUI();

  let lastTime = performance.now();

  function animate(now) {
    if (!isGrabAnimating) return;

    const deltaSec = (now - lastTime) / 1000;
    lastTime = now;

    const stepSpeed = 0.08 * grabSpeedMultiplier;
    grabProgress += deltaSec * stepSpeed;

    if (grabProgress >= 1) {
      grabProgress = 1;
      isGrabAnimating = false;
      showArrivalBanner(targetBuildingName);
    }

    const state = getInterpolatedPointAndAngle(currentRouteCoords, grabProgress);

    if (grabRiderMarker) {
      grabRiderMarker.setLatLng([state.lat, state.lng]);
      grabRiderMarker.setIcon(createGrabRiderIcon(activeTravelMode, state.angle));
    } else {
      grabRiderMarker = L.marker([state.lat, state.lng], {
        icon: createGrabRiderIcon(activeTravelMode, state.angle),
        zIndexOffset: 1000
      }).addTo(map);
    }

    const followCam = document.getElementById("chk-grab-follow-cam")?.checked;
    if (followCam && map) {
      map.panTo([state.lat, state.lng], { animate: true, duration: 0.1 });
    }

    updateGrabMotionUI();

    if (isGrabAnimating) {
      grabAnimId = requestAnimationFrame(animate);
    }
  }

  grabAnimId = requestAnimationFrame(animate);
}

function pauseGrabRiderMotion() {
  isGrabAnimating = false;
  if (grabAnimId) cancelAnimationFrame(grabAnimId);
  updateGrabMotionUI();
}

function resetGrabRiderMotion() {
  pauseGrabRiderMotion();
  grabProgress = 0;
  if (currentRouteCoords.length > 0) {
    const startPt = currentRouteCoords[0];
    if (grabRiderMarker) {
      grabRiderMarker.setLatLng(startPt);
      grabRiderMarker.setIcon(createGrabRiderIcon(activeTravelMode, 0));
    }
  }
  updateGrabMotionUI();
}

function showArrivalBanner(bName) {
  let banner = document.getElementById("arrival-toast-banner");
  if (!banner) {
    banner = document.createElement("div");
    banner.id = "arrival-toast-banner";
    banner.className = "arrival-toast-banner";
    document.body.appendChild(banner);
  }
  banner.innerHTML = `<i class="fa-solid fa-flag-checkered fa-lg"></i> ถึงจุดหมายปลายทาง <strong>${bName || 'อาคาร'}</strong> เรียบร้อยแล้ว!`;
  banner.classList.add("show");
  setTimeout(() => {
    banner.classList.remove("show");
  }, 4500);
}

function calculateWalkingRoute() {
  const srcVal = document.getElementById("select-nav-source").value;
  const destVal = document.getElementById("select-nav-dest").value;
  const resultPanel = document.getElementById("nav-results-wrapper");
  const stepsContainer = document.getElementById("nav-route-steps-container");

  // Clean existing route and motion
  pauseGrabRiderMotion();
  if (grabRiderMarker) {
    map.removeLayer(grabRiderMarker);
    grabRiderMarker = null;
  }
  if (routePolyline) {
    map.removeLayer(routePolyline);
    routePolyline = null;
  }

  if (!srcVal || !destVal) {
    resultPanel.classList.remove("active");
    return;
  }

  if (srcVal === destVal) {
    showToast("จุดเริ่มต้นและปลายทางเป็นอาคารเดียวกัน");
    resultPanel.classList.remove("active");
    return;
  }

  let startNodeId = null;
  let customGPSLeg = null;

  if (srcVal === "my_location") {
    if (!userPixelCoords) {
      showModal(
        "ไม่พบตำแหน่ง GPS",
        "กรุณากดปุ่มระบุตำแหน่งปัจจุบัน (รูปเป้าชี้ขวาบน) เพื่อระบุตำแหน่งคุณบนแผนผังเสียก่อน หรือระบุจุดเริ่มต้นเป็นอาคารตึกด้านล่างแทน",
        "warning"
      );
      document.getElementById("select-nav-source").value = "";
      resultPanel.classList.remove("active");
      return;
    }

    let closestNode = null;
    let minDist = Infinity;

    adminBuildings.forEach(b => {
      const dx = userPixelCoords[1] - b.coords[1];
      const dy = userPixelCoords[0] - b.coords[0];
      const d = Math.sqrt(dx * dx + dy * dy);
      if (d < minDist) {
        minDist = d;
        closestNode = b.id;
      }
    });

    startNodeId = closestNode;
    customGPSLeg = {
      from: userPixelCoords,
      to: adminBuildings.find(b => b.id === closestNode).coords,
      distance: minDist
    };
  } else {
    startNodeId = Number(srcVal);
  }

  const endNodeId = Number(destVal);
  const endBuilding = adminBuildings.find(b => b.id === endNodeId);
  targetBuildingName = endBuilding ? endBuilding.name : "";

  const result = solveDijkstra(startNodeId, endNodeId);

  if (result.path.length === 0) {
    showToast("ไม่สามารถหาเส้นทางนำทางได้");
    resultPanel.classList.remove("active");
    return;
  }

  currentRouteCoords = [];
  if (customGPSLeg) {
    currentRouteCoords.push(customGPSLeg.from);
  }

  result.path.forEach(id => {
    const coords = getNodeCoords(id);
    if (coords) currentRouteCoords.push(coords);
  });

  // Google Maps Glowing Polyline
  routePolyline = L.polyline(currentRouteCoords, {
    color: '#00B14F',
    weight: 7,
    opacity: 0.9,
    lineJoin: 'round',
    dashArray: '10, 10',
    className: 'glowing-polyline'
  }).addTo(map);

  map.fitBounds(routePolyline.getBounds(), { padding: [60, 60] });

  let totalDistancePixels = result.distance;
  if (customGPSLeg) {
    totalDistancePixels += customGPSLeg.distance;
  }

  const totalDistanceMeters = Math.round(totalDistancePixels * 0.65);
  const modeInfo = TRAVEL_MODES[activeTravelMode] || TRAVEL_MODES.walk;
  const totalSeconds = totalDistanceMeters / modeInfo.mps;
  const totalMinutes = Math.max(1, Math.round(totalSeconds / 60));

  document.getElementById("nav-summary-distance").textContent = `${totalDistanceMeters} เมตร`;
  document.getElementById("nav-summary-time").textContent = `${totalMinutes} นาที (${modeInfo.label})`;

  stepsContainer.innerHTML = "";

  if (customGPSLeg) {
    const startB = adminBuildings.find(b => b.id === startNodeId);
    const startBNum = startB.id === 21 ? "C" : startB.id;
    const stepCard = document.createElement("div");
    stepCard.className = "nav-step-item";
    stepCard.innerHTML = `
      <div class="nav-step-icon start"><i class="fa-solid fa-location-arrow" style="color:#fff; font-size:10px;"></i></div>
      <div class="nav-step-text">
        เริ่มต้นจาก <strong>ตำแหน่งปัจจุบันของคุณ (GPS)</strong> เดินไปยัง <strong>ตึก ${startBNum}. ${startB.name}</strong> (${Math.round(customGPSLeg.distance * 0.65)} ม.)
      </div>
    `;
    stepsContainer.appendChild(stepCard);
  }

  const buildingNodes = result.path.filter(id => typeof id === 'number' || !isNaN(Number(id)));
  buildingNodes.forEach((nodeId, idx) => {
    const b = adminBuildings.find(item => item.id === Number(nodeId));
    if (!b) return;
    const bNum = b.id === 21 ? "C" : b.id;

    const stepCard = document.createElement("div");
    stepCard.className = "nav-step-item";

    let iconClass = "node";
    let stepTitle = `เดินทางตามถนนผ่าน <strong>ตึก ${bNum}. ${b.name}</strong>`;

    if (idx === 0 && !customGPSLeg) {
      iconClass = "start";
      stepTitle = `เริ่มต้นออกจาก <strong>ตึก ${bNum}. ${b.name}</strong>`;
    } else if (idx === buildingNodes.length - 1) {
      iconClass = "end";
      stepTitle = `ถึงจุดหมายปลายทาง <strong>ตึก ${bNum}. ${b.name}</strong>`;
    }

    stepCard.innerHTML = `
      <div class="nav-step-icon ${iconClass}"></div>
      <div class="nav-step-text">${stepTitle}</div>
    `;
    stepsContainer.appendChild(stepCard);
  });

  resultPanel.classList.add("active");
  trackEvent('navigate', targetBuildingName);
}

// ─── Real Google Maps Navigation Trigger ─────────────────────────────
function startActiveTurnByTurnNav() {
  const srcVal = document.getElementById("select-nav-source").value;
  const destVal = document.getElementById("select-nav-dest").value;

  if (!destVal) {
    showToast("กรุณาเลือกจุดหมายปลายทางก่อนเริ่มนำทาง");
    return;
  }

  const destBuilding = adminBuildings.find(b => b.id === Number(destVal));
  if (!destBuilding || !destBuilding.realCoords) {
    showToast("ไม่พบพิกัดจุดหมายปลายทาง");
    return;
  }

  const travelModeMap = {
    walk: 'walking',
    bike: 'bicycling',
    motorcycle: 'two-wheeler',
    car: 'driving'
  };
  const gmode = travelModeMap[activeTravelMode] || 'walking';
  let gmapsUrl = '';

  if (srcVal === "my_location") {
    gmapsUrl = `https://www.google.com/maps/dir/?api=1&destination=${destBuilding.realCoords[0]},${destBuilding.realCoords[1]}&travelmode=${gmode}`;
  } else {
    const srcBuilding = adminBuildings.find(b => b.id === Number(srcVal));
    if (srcBuilding && srcBuilding.realCoords) {
      gmapsUrl = `https://www.google.com/maps/dir/?api=1&origin=${srcBuilding.realCoords[0]},${srcBuilding.realCoords[1]}&destination=${destBuilding.realCoords[0]},${destBuilding.realCoords[1]}&travelmode=${gmode}`;
    } else {
      gmapsUrl = `https://www.google.com/maps/dir/?api=1&destination=${destBuilding.realCoords[0]},${destBuilding.realCoords[1]}&travelmode=${gmode}`;
    }
  }

  trackEvent('navigate', destBuilding.name);
  window.open(gmapsUrl, '_blank');
}

function stopActiveTurnByTurnNav() {
  isNavActive = false;
  if (navAnimId) cancelAnimationFrame(navAnimId);
  if (navAnimMarker) { map.removeLayer(navAnimMarker); navAnimMarker = null; }
  document.getElementById("nav-hud-overlay").style.display = "none";
  document.getElementById("carousel-panel").style.display = "block";
}

function startDirectNavigationToBuilding(bId) {
  closeInfoPanel();
  document.getElementById("nav-routes-panel").classList.add("active");
  const sourceSel = document.getElementById("select-nav-source");
  const destSel = document.getElementById("select-nav-dest");

  if (!sourceSel.value) {
    sourceSel.value = userPixelCoords ? "my_location" : (adminBuildings[0]?.id || "1");
  }
  destSel.value = bId;
  calculateWalkingRoute();
}

function closeNavigationPanel() {
  stopActiveTurnByTurnNav();
  if (routePolyline) {
    map.removeLayer(routePolyline);
    routePolyline = null;
  }
  document.getElementById("nav-routes-panel").classList.remove("active");
  document.getElementById("select-nav-source").value = "";
  document.getElementById("select-nav-dest").value = "";
  document.getElementById("nav-results-wrapper").classList.remove("active");
}

/* ==========================================================================
   Admin Logic Core Methods
   ========================================================================== */

async function saveBuildingsToStorage(actionType = null, buildingItem = null) {
  localStorage.setItem("sskru_buildings", JSON.stringify(adminBuildings));
  buildNetworkGraph();
  populateDropdownSelectors();
  renderBuildingCarousel(adminBuildings);

  if (document.getElementById("admin-dashboard-overlay")?.classList.contains("active")) {
    renderAdminDashboardTable();
  }

  // Sync to Backend REST API if server is online
  if (isServerConnected && actionType && buildingItem) {
    try {
      let url = '/api/buildings';
      let method = 'POST';

      if (actionType === 'PUT') {
        url = `/api/buildings/${buildingItem.id}`;
        method = 'PUT';
      } else if (actionType === 'DELETE') {
        url = `/api/buildings/${buildingItem.id}`;
        method = 'DELETE';
      }

      const opts = {
        method: method,
        headers: { 'Content-Type': 'application/json' }
      };

      if (actionType !== 'DELETE') {
        opts.body = JSON.stringify(buildingItem);
      }

      const res = await fetch(url, opts);
      const resData = await res.json();
      if (resData.success) {
        console.log("Synced change with backend:", resData.message);
      }
    } catch (e) {
      console.error("Failed to sync change with backend API", e);
    }
  }
}

// Enter Admin Mode & Enable draggable points
function enterAdminMode() {
  isAdminMode = true;
  document.querySelector(".app-container").classList.add("admin-active");
  document.getElementById("admin-panel").style.display = "flex";

  // Close standard info/nav panels to prevent layout clashes
  closeInfoPanel();
  closeNavigationPanel();

  // Redraw all markers as draggable
  renderMarkers();
  showToast("เข้าสู่โหมดแอดมิน: สามารถลากมาร์กเกอร์เพื่อย้ายตำแหน่ง หรือเปิดตารางหลังบ้านเพื่อจัดการข้อมูล");
}

// Exit Admin Mode & Save
function exitAdminMode() {
  isAdminMode = false;
  document.querySelector(".app-container").classList.remove("admin-active");
  document.getElementById("admin-panel").style.display = "none";

  // Save local updates & redraw static markers
  saveBuildingsToStorage();
  renderMarkers();
  showToast("ออกจากโหมดแอดมินเรียบร้อย");
}

// Form management - open edit form
function openEditBuildingForm(b) {
  const displayNum = b.id === 21 ? "C" : b.id;

  document.getElementById("building-form-title").innerHTML = `<i class="fa-solid fa-edit"></i> แก้ไขข้อมูลอาคาร: ตึก ${displayNum}`;
  document.getElementById("edit-building-id").value = b.id;
  document.getElementById("edit-building-num").value = displayNum;
  document.getElementById("edit-building-category").value = b.category;
  document.getElementById("edit-building-name").value = b.name;
  document.getElementById("edit-building-name-en").value = b.nameEn;
  document.getElementById("edit-building-desc").value = b.description || "";
  document.getElementById("edit-building-phone").value = b.phone || "";
  document.getElementById("edit-building-coords").value = `[${b.coords[0]}, ${b.coords[1]}]`;
  document.getElementById("edit-building-real-coords").value = b.realCoords ? `${b.realCoords[0]}, ${b.realCoords[1]}` : "";

  document.getElementById("btn-building-delete").style.display = "block";
  document.getElementById("building-form-overlay").classList.add("active");
}

// Form management - open create form
function openAddBuildingForm(y, x) {
  const nextId = adminBuildings.length > 0
    ? Math.max(...adminBuildings.map(b => typeof b.id === 'number' ? b.id : 0)) + 1
    : 1;

  document.getElementById("building-form-title").innerHTML = `<i class="fa-solid fa-plus-circle"></i> เพิ่มอาคารใหม่ ณ พิกัด [${y}, ${x}]`;
  document.getElementById("edit-building-id").value = "NEW";
  document.getElementById("edit-building-num").value = nextId;
  document.getElementById("edit-building-category").value = "academic";
  document.getElementById("edit-building-name").value = "";
  document.getElementById("edit-building-name-en").value = "";
  document.getElementById("edit-building-desc").value = "";
  document.getElementById("edit-building-phone").value = "";
  document.getElementById("edit-building-coords").value = `[${y}, ${x}]`;

  const lat = LAT1 + (y - Y1) / KY;
  const lng = LNG1 + (x - X1) / KX;
  document.getElementById("edit-building-real-coords").value = `${lat.toFixed(6)}, ${lng.toFixed(6)}`;

  document.getElementById("btn-building-delete").style.display = "none";
  document.getElementById("building-form-overlay").classList.add("active");
}

function handleBuildingFormSubmit(e) {
  e.preventDefault();

  const idVal = document.getElementById("edit-building-id").value;
  const numInput = document.getElementById("edit-building-num").value.trim();
  const category = document.getElementById("edit-building-category").value;
  const name = document.getElementById("edit-building-name").value.trim();
  const nameEn = document.getElementById("edit-building-name-en").value.trim();
  const description = document.getElementById("edit-building-desc").value.trim();
  const phone = document.getElementById("edit-building-phone").value.trim();
  const coordsStr = document.getElementById("edit-building-coords").value;
  const realCoordsStr = document.getElementById("edit-building-real-coords").value.trim();

  const coords = coordsStr.replace(/[\[\]\s]/g, "").split(",").map(Number);
  const realCoords = realCoordsStr.split(",").map(Number);

  if (realCoords.length !== 2 || isNaN(realCoords[0]) || isNaN(realCoords[1])) {
    alert("กรุณาระบุพิกัด GPS จริงให้ถูกต้องในรูปแบบ: lat, lng");
    return;
  }

  let id = idVal === "NEW" ? (adminBuildings.length + 100) : Number(idVal);
  if (numInput === "C" || numInput === "c") {
    id = 21;
  } else if (!isNaN(numInput)) {
    if (idVal === "NEW") id = Number(numInput);
  }

  const newB = {
    id: id,
    name: name,
    nameEn: nameEn,
    category: category,
    coords: coords,
    realCoords: realCoords,
    description: description,
    phone: phone,
    tags: [numInput.toLowerCase(), name.toLowerCase(), nameEn.toLowerCase()]
  };

  let actionType = 'PUT';

  if (idVal === "NEW") {
    actionType = 'POST';
    if (adminBuildings.some(b => b.id === id)) {
      alert(`รหัสตึก/มาร์กเกอร์ '${numInput}' ซ้ำกับตึกอื่นที่มีอยู่แล้ว กรุณาเปลี่ยนใหม่`);
      return;
    }
    adminBuildings.push(newB);
    showToast(`เพิ่มอาคารใหม่ ${name} เรียบร้อยแล้ว`);
  } else {
    const idx = adminBuildings.findIndex(b => b.id === Number(idVal));
    if (idx !== -1) {
      adminBuildings[idx] = newB;
      showToast(`อัปเดตข้อมูลตึก ${numInput} สำเร็จ`);
    }
  }

  saveBuildingsToStorage(actionType, newB);
  renderMarkers();
  document.getElementById("building-form-overlay").classList.remove("active");
}

function handleBuildingDelete() {
  const idVal = document.getElementById("edit-building-id").value;
  if (idVal === "NEW") return;

  const targetId = Number(idVal);
  const targetBuilding = adminBuildings.find(b => b.id === targetId);
  const confirmDel = confirm("คุณต้องการลบตึกนี้ออกจากแผนที่ใช่หรือไม่? การกระทำนี้ไม่สามารถย้อนกลับได้");
  if (!confirmDel) return;

  adminBuildings = adminBuildings.filter(b => b.id !== targetId);
  saveBuildingsToStorage('DELETE', targetBuilding || { id: targetId });
  renderMarkers();

  document.getElementById("building-form-overlay").classList.remove("active");
  showToast("ลบตึกอาคารสำเร็จ");
}

// Show JSON configuration export modal
function openExportModal() {
  const textarea = document.getElementById("export-textarea");
  const codeString = "const BUILDINGS = " + JSON.stringify(adminBuildings, null, 2) + ";";
  textarea.value = codeString;
  document.getElementById("export-modal-overlay").classList.add("active");
}

/* ==========================================================================
   Admin Backend Data Dashboard Rendering
   ========================================================================== */

function openAdminDashboard() {
  renderAdminDashboardTable();
  document.getElementById("admin-dashboard-overlay").classList.add("active");
}

function renderAdminDashboardTable() {
  const tbody = document.getElementById("dash-table-body");
  const query = (document.getElementById("dash-search-input")?.value || "").trim().toLowerCase();
  
  if (!tbody) return;
  tbody.innerHTML = "";

  const filtered = adminBuildings.filter(b => {
    return !query || 
      b.name.toLowerCase().includes(query) ||
      b.nameEn.toLowerCase().includes(query) ||
      b.id.toString().includes(query) ||
      b.category.toLowerCase().includes(query);
  });

  // Update stats
  document.getElementById("dash-total-buildings").textContent = adminBuildings.length;
  document.getElementById("dash-academic-count").textContent = adminBuildings.filter(b => b.category === 'academic').length;
  document.getElementById("dash-office-count").textContent = adminBuildings.filter(b => b.category === 'office').length;
  document.getElementById("dash-facility-count").textContent = adminBuildings.filter(b => b.category === 'facility').length;
  document.getElementById("dash-library-count").textContent = adminBuildings.filter(b => b.category === 'library').length;

  if (filtered.length === 0) {
    tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding: 20px; color: var(--text-secondary);">ไม่พบข้อมูลอาคารที่ค้นหา</td></tr>`;
    return;
  }

  [...filtered].sort((a,b) => a.id - b.id).forEach(b => {
    const displayNum = b.id === 21 ? "C" : b.id;
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><strong>${displayNum}</strong></td>
      <td><strong>${b.name}</strong></td>
      <td style="color:var(--text-secondary); font-size:11px;">${b.nameEn}</td>
      <td><span class="dash-tag-cat ${b.category}">${translateCategory(b.category)}</span></td>
      <td><code>[${b.coords[0]}, ${b.coords[1]}]</code></td>
      <td style="font-size:11px;">${b.realCoords ? b.realCoords.join(', ') : '-'}</td>
      <td style="font-size:11px;">${b.phone || '-'}</td>
      <td style="text-align:center;">
        <button class="table-btn edit" title="แก้ไข" data-id="${b.id}"><i class="fa-solid fa-pen-to-square"></i></button>
        <button class="table-btn delete" title="ลบ" data-id="${b.id}"><i class="fa-solid fa-trash-can"></i></button>
      </td>
    `;

    tr.querySelector(".table-btn.edit").onclick = () => openEditBuildingForm(b);
    tr.querySelector(".table-btn.delete").onclick = () => {
      if (confirm(`คุณต้องการลบอาคาร "${b.name}" ใช่หรือไม่?`)) {
        adminBuildings = adminBuildings.filter(item => item.id !== b.id);
        saveBuildingsToStorage('DELETE', b);
        renderMarkers();
        renderAdminDashboardTable();
        showToast(`ลบอาคาร ${b.name} ออกจากระบบแล้ว`);
      }
    };

    tbody.appendChild(tr);
  });
}

/* ==========================================================================
   Event Bindings
   ========================================================================== */
function setupEventListeners() {
  document.getElementById("category-filter").addEventListener("click", (e) => {
    const tab = e.target.closest(".category-tab");
    if (tab) {
      filterByCategory(tab.getAttribute("data-category"));
    }
  });

  const searchInput = document.getElementById("search-input");
  searchInput.addEventListener("input", handleSearchInput);
  searchInput.addEventListener("focus", handleSearchInput);

  document.addEventListener("click", (e) => {
    if (!e.target.closest(".nav-search-wrapper")) {
      document.getElementById("search-suggestions").style.display = "none";
    }
  });

  document.getElementById("btn-search-clear").onclick = () => {
    searchInput.value = "";
    document.getElementById("search-suggestions").style.display = "none";
    document.getElementById("btn-search-clear").style.display = "none";
    document.getElementById("search-input").focus();
  };

  document.getElementById("btn-panel-close").onclick = closeInfoPanel;
  document.getElementById("btn-nav-panel-close").onclick = closeNavigationPanel;

  document.getElementById("btn-nav-trigger").onclick = () => {
    document.getElementById("nav-routes-panel").classList.add("active");
    closeInfoPanel();
  };

  document.getElementById("btn-univ-info-trigger").onclick = () => {
    showModal(
      "มหาวิทยาลัยราชภัฏศรีสะเกษ (SSKRU)",
      `ที่ตั้ง: เลขที่ 319 ถนนไทยพันทา ตำบลโพธิ์ อำเภอเมือง จังหวัดศรีสะเกษ รหัสไปรษณีย์ 33000

เบอร์โทรศัพท์: 045-643-600
อีเมล: webmaster@sskru.ac.th

พื้นที่จัดการศึกษา: มีเนื้อที่ประมาณ 525 ไร่ 2 งาน 32 ตารางวา ในเขตเทศบาลเมืองศรีสะเกษ`,
      "info"
    );
  };

  // ============ SIDE DRAWER ============
  document.getElementById("btn-hamburger").onclick = () => openSideDrawer();
  document.getElementById("btn-drawer-close").onclick = () => closeSideDrawer();
  document.getElementById("drawer-backdrop").onclick = () => closeSideDrawer();

  document.getElementById("btn-drawer-nav").onclick = () => {
    closeSideDrawer();
    document.getElementById("nav-routes-panel").classList.add("active");
    closeInfoPanel();
  };

  document.getElementById("btn-drawer-my-location").onclick = () => {
    closeSideDrawer();
    trackUserLocation();
  };

  document.getElementById("btn-drawer-info").onclick = () => {
    closeSideDrawer();
    document.getElementById("btn-univ-info-trigger").click();
  };

  const btnDrawerAdmin = document.getElementById("btn-drawer-admin");
  if (btnDrawerAdmin) {
    btnDrawerAdmin.onclick = () => {
      closeSideDrawer();
      window.location.href = "/admin/";
    };
  }

  document.getElementById("btn-drawer-share").onclick = () => {
    closeSideDrawer();
    const shareData = {
      title: "SSKRU Campus Map",
      text: "ระบบแผนผังนำทาง 3D มหาวิทยาลัยราชภัฏศรีสะเกษ",
      url: window.location.href
    };
    if (navigator.share) {
      navigator.share(shareData).catch(() => {});
    } else {
      navigator.clipboard.writeText(window.location.href);
      showToast("คัดลอกลิงก์แล้ว!");
    }
  };

  // ============ MOBILE SEARCH PANEL ============
  const mobileSearchPanel = document.getElementById("mobile-search-panel");
  const mobileInput = document.getElementById("search-input-mobile");
  const mobileDropdown = document.getElementById("search-suggestions-mobile");
  const mobileClear = document.getElementById("btn-search-clear-mobile");

  document.getElementById("btn-mobile-search").onclick = () => {
    mobileSearchPanel.classList.add("active");
    setTimeout(() => mobileInput?.focus(), 100);
  };

  document.getElementById("btn-mobile-search-close").onclick = () => {
    mobileSearchPanel.classList.remove("active");
  };

  document.getElementById("btn-nav-trigger-mobile")?.addEventListener("click", () => {
    document.getElementById("nav-routes-panel").classList.add("active");
    closeInfoPanel();
  });

  if (mobileInput) {
    mobileInput.addEventListener("input", (e) => handleMobileSearchInput(e, mobileDropdown));
    mobileInput.addEventListener("focus", (e) => handleMobileSearchInput(e, mobileDropdown));
  }

  if (mobileClear) {
    mobileClear.onclick = () => {
      if (mobileInput) mobileInput.value = "";
      mobileDropdown.style.display = "none";
      mobileClear.style.display = "none";
    };
  }

  // ============ INFO PANEL TABS ============
  const infoPanelEl = document.getElementById("building-info-panel");
  document.querySelectorAll(".info-tab-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const tabId = btn.getAttribute("data-tab");
      document.querySelectorAll(".info-tab-btn").forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".info-tab-pane").forEach(p => p.classList.remove("active"));
      btn.classList.add("active");
      const pane = document.getElementById(`tab-${tabId}`);
      if (pane) pane.classList.add("active");
    });
  });

  // ============ SWIPE GESTURE — Bottom Sheets ============
  setupSwipeGesture(infoPanelEl, () => closeInfoPanel());
  const navPanelEl = document.getElementById("nav-routes-panel");
  setupSwipeGesture(navPanelEl, () => closeNavigationPanel());

  document.getElementById("btn-logo-reset").onclick = () => {
    closeInfoPanel();
    closeNavigationPanel();
    map.setView(IMAGE_CENTER, -1, { animate: true });
  };

  document.getElementById("select-nav-source").onchange = calculateWalkingRoute;
  document.getElementById("select-nav-dest").onchange = calculateWalkingRoute;

  document.getElementById("btn-modal-ok").onclick = () => {
    document.getElementById("custom-modal-overlay").classList.remove("active");
  };

  document.getElementById("btn-map-zoom-in").onclick = () => map.zoomIn();
  document.getElementById("btn-map-zoom-out").onclick = () => map.zoomOut();
  document.getElementById("btn-map-my-location").onclick = trackUserLocation;

  document.getElementById("btn-map-reset").onclick = () => {
    map.fitBounds(IMAGE_BOUNDS, { padding: [15, 15] });
  };

  // Active Navigation HUD controls
  document.getElementById("btn-start-active-nav")?.addEventListener("click", startActiveTurnByTurnNav);
  document.getElementById("btn-hud-stop")?.addEventListener("click", stopActiveTurnByTurnNav);

  // View mode switcher pill
  const btnView3D = document.getElementById("btn-view-3d");
  const btnViewAerial = document.getElementById("btn-view-aerial");

  if (btnView3D && btnViewAerial) {
    btnView3D.onclick = () => {
      btnView3D.classList.add("active");
      btnViewAerial.classList.remove("active");
      document.getElementById("map").classList.remove("aerial-mode");
      closeNavigationPanel();
      map.fitBounds(IMAGE_BOUNDS, { padding: [15, 15] });
    };

    btnViewAerial.onclick = () => {
      btnViewAerial.classList.add("active");
      btnView3D.classList.remove("active");
      document.getElementById("map").classList.add("aerial-mode");
      showToast("สลับเข้าสู่มุมมองนำทางมุมสูง (Google Maps Style)");
      if (document.getElementById("select-nav-source").value && document.getElementById("select-nav-dest").value) {
        calculateWalkingRoute();
      } else {
        map.fitBounds(IMAGE_BOUNDS, { padding: [25, 25] });
      }
    };
  }

  // Travel mode tabs
  const travelModeSelector = document.getElementById("travel-mode-selector");
  if (travelModeSelector) {
    travelModeSelector.addEventListener("click", (e) => {
      const btn = e.target.closest(".travel-mode-btn");
      if (btn) {
        document.querySelectorAll(".travel-mode-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        activeTravelMode = btn.getAttribute("data-mode") || 'walk';
        if (document.getElementById("select-nav-source").value && document.getElementById("select-nav-dest").value) {
          calculateWalkingRoute();
        }
      }
    });
  }
}

// Bind admin action events
function setupAdminEventListeners() {
  const loginOverlay = document.getElementById("admin-login-overlay");
  const loginForm = document.getElementById("admin-login-form");
  const btnAdminLogin = document.getElementById("btn-admin-login");

  if (btnAdminLogin) {
    btnAdminLogin.onclick = () => {
      window.location.href = "/admin/";
    };
  }

  if (loginForm && loginOverlay) {
    document.getElementById("btn-admin-login-cancel")?.addEventListener("click", () => {
      loginOverlay.classList.remove("active");
    });
  }

  const btnAdminDashboard = document.getElementById("btn-admin-dashboard");
  if (btnAdminDashboard) btnAdminDashboard.onclick = openAdminDashboard;
  document.getElementById("btn-dash-close")?.addEventListener("click", () => {
    document.getElementById("admin-dashboard-overlay")?.classList.remove("active");
  });
  document.getElementById("btn-dash-add")?.addEventListener("click", () => {
    openAddBuildingForm(512, 768);
  });
  document.getElementById("btn-admin-export")?.addEventListener("click", openExportModal);
  document.getElementById("dash-search-input")?.addEventListener("input", renderAdminDashboardTable);
}


/* ==========================================================================
   v2.0 — Side Drawer, Smart Navigation, Mobile Search, Swipe Gesture
   ========================================================================== */

function openSideDrawer() {
  document.getElementById("side-drawer").classList.add("open");
  document.getElementById("drawer-backdrop").classList.add("active");
  document.body.style.overflow = 'hidden';
}

function closeSideDrawer() {
  document.getElementById("side-drawer").classList.remove("open");
  document.getElementById("drawer-backdrop").classList.remove("active");
  document.body.style.overflow = '';
}

/**
 * Smart Navigation: Opens in-app route for desktop,
 * or external maps app for mobile (Android → Google Maps, iOS → Apple Maps)
 */
function openSmartNavigation(b) {
  const lat = b.realCoords[0];
  const lng = b.realCoords[1];

  const travelModeMap = {
    walk: 'walking',
    bike: 'bicycling',
    motorcycle: 'two-wheeler',
    car: 'driving'
  };
  const gmode = travelModeMap[activeTravelMode] || 'walking';
  const gmapsUrl = `https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}&travelmode=${gmode}`;

  trackEvent('navigate', b.name);
  window.open(gmapsUrl, '_blank');
}

/**
 * Mobile search input handler for the mobile search panel
 */
function handleMobileSearchInput(e, dropdown) {
  const query = e.target.value.trim().toLowerCase();
  const clearBtn = document.getElementById("btn-search-clear-mobile");

  if (!query) {
    dropdown.style.display = "none";
    if (clearBtn) clearBtn.style.display = "none";
    return;
  }

  if (clearBtn) clearBtn.style.display = "flex";

  const matches = adminBuildings.filter(b =>
    b.name.toLowerCase().includes(query) ||
    b.nameEn.toLowerCase().includes(query) ||
    b.id.toString() === query ||
    (b.id === 21 && query === "c") ||
    b.tags.some(t => t.toLowerCase().includes(query))
  );

  dropdown.innerHTML = "";

  if (matches.length === 0) {
    dropdown.innerHTML = `<div style="padding: 15px; text-align: center; color: var(--text-secondary); font-size: 13px;"><i class="fa-solid fa-circle-question"></i> ไม่พบอาคารที่ค้นหา</div>`;
    dropdown.style.display = "block";
    return;
  }

  matches.forEach(b => {
    const displayNum = b.id === 21 ? "C" : b.id;
    const item = document.createElement("div");
    item.className = "autocomplete-item";
    item.innerHTML = `
      <div class="autocomplete-icon">${displayNum}</div>
      <div class="autocomplete-text">
        <div class="autocomplete-title">${b.name}</div>
        <div class="autocomplete-subtitle">${b.nameEn}</div>
      </div>
    `;
    item.onclick = () => {
      selectBuilding(b);
      document.getElementById("mobile-search-panel").classList.remove("active");
      dropdown.style.display = "none";
    };
    dropdown.appendChild(item);
  });

  dropdown.style.display = "block";
}

/**
 * Setup swipe-down gesture to dismiss a bottom sheet panel
 * @param {HTMLElement} panelEl - The panel element
 * @param {Function} closeCallback - Function to call when dismissed
 */
function setupSwipeGesture(panelEl, closeCallback) {
  if (!panelEl) return;

  let startY = 0;
  let startX = 0;
  let isDragging = false;

  panelEl.addEventListener("touchstart", (e) => {
    // Only trigger from drag handle or panel header
    const handle = panelEl.querySelector(".panel-drag-handle, .info-panel-drag-handle");
    if (handle && handle.contains(e.target)) {
      startY = e.touches[0].clientY;
      startX = e.touches[0].clientX;
      isDragging = true;
    }
  }, { passive: true });

  panelEl.addEventListener("touchmove", (e) => {
    if (!isDragging) return;
    const dy = e.touches[0].clientY - startY;
    const dx = Math.abs(e.touches[0].clientX - startX);
    // Vertical swipe only
    if (dy > 0 && dy > dx) {
      panelEl.style.transform = `translateY(${dy}px)`;
    }
  }, { passive: true });

  panelEl.addEventListener("touchend", (e) => {
    if (!isDragging) return;
    isDragging = false;
    const dy = e.changedTouches[0].clientY - startY;
    panelEl.style.transform = '';
    if (dy > 80) {
      closeCallback();
    }
  }, { passive: true });
}

