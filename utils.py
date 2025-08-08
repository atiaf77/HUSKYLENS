"""
أدوات مساعدة للعمل مع HUSKYLENS
Utility functions for HUSKYLENS operations
"""

import cv2
import numpy as np
from typing import List, Tuple
import json
import os
from datetime import datetime

class HuskyLensUtils:
    """أدوات مساعدة للعمل مع HUSKYLENS"""
    
    @staticmethod
    def draw_detection_box(image: np.ndarray, x: int, y: int, width: int, height: int, 
                          label: str = "", color: Tuple[int, int, int] = (0, 255, 0)) -> np.ndarray:
        """رسم مربع حول الكائن المكتشف"""
        # رسم المستطيل
        cv2.rectangle(image, (x, y), (x + width, y + height), color, 2)
        
        # إضافة النص
        if label:
            cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        return image
    
    @staticmethod
    def draw_center_point(image: np.ndarray, x: int, y: int, 
                         color: Tuple[int, int, int] = (255, 0, 0)) -> np.ndarray:
        """رسم نقطة في مركز الكائن"""
        cv2.circle(image, (x, y), 5, color, -1)
        return image
    
    @staticmethod
    def draw_arrow(image: np.ndarray, start: Tuple[int, int], end: Tuple[int, int],
                   color: Tuple[int, int, int] = (0, 0, 255)) -> np.ndarray:
        """رسم سهم للاتجاه"""
        cv2.arrowedLine(image, start, end, color, 2, tipLength=0.3)
        return image
    
    @staticmethod
    def calculate_distance(point1: Tuple[int, int], point2: Tuple[int, int]) -> float:
        """حساب المسافة بين نقطتين"""
        return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    @staticmethod
    def get_object_area(width: int, height: int) -> int:
        """حساب مساحة الكائن"""
        return width * height
    
    @staticmethod
    def is_object_in_region(obj_x: int, obj_y: int, region_x: int, region_y: int,
                           region_width: int, region_height: int) -> bool:
        """تحقق من وجود الكائن في منطقة معينة"""
        return (region_x <= obj_x <= region_x + region_width and 
                region_y <= obj_y <= region_y + region_height)
    
    @staticmethod
    def save_detection_log(detections: List[dict], filename: str = None):
        """حفظ سجل الكشوفات في ملف JSON"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"huskylens_log_{timestamp}.json"
        
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "total_detections": len(detections),
            "detections": detections
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
        
        print(f"📝 تم حفظ السجل في: {filename}")
    
    @staticmethod
    def load_detection_log(filename: str) -> dict:
        """تحميل سجل الكشوفات من ملف JSON"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ الملف غير موجود: {filename}")
            return {}
        except json.JSONDecodeError:
            print(f"❌ خطأ في قراءة الملف: {filename}")
            return {}

class ObjectTracker:
    """متتبع الكائنات لتتبع حركة الكائنات عبر الإطارات"""
    
    def __init__(self, max_history: int = 10):
        self.max_history = max_history
        self.tracked_objects = {}
        self.next_id = 1
    
    def update(self, detections: List[Tuple[int, int, int, int]]) -> dict:
        """تحديث الكائنات المتتبعة"""
        current_frame = {}
        
        for detection in detections:
            x, y, w, h = detection
            center_x = x + w // 2
            center_y = y + h // 2
            
            # البحث عن أقرب كائن متتبع
            best_match_id = None
            min_distance = float('inf')
            
            for obj_id, history in self.tracked_objects.items():
                if history:
                    last_pos = history[-1]
                    distance = np.sqrt((center_x - last_pos[0])**2 + (center_y - last_pos[1])**2)
                    
                    if distance < min_distance and distance < 50:  # عتبة المسافة
                        min_distance = distance
                        best_match_id = obj_id
            
            # إضافة الكائن
            if best_match_id is not None:
                # كائن موجود
                self.tracked_objects[best_match_id].append((center_x, center_y))
                if len(self.tracked_objects[best_match_id]) > self.max_history:
                    self.tracked_objects[best_match_id].pop(0)
                current_frame[best_match_id] = (x, y, w, h)
            else:
                # كائن جديد
                self.tracked_objects[self.next_id] = [(center_x, center_y)]
                current_frame[self.next_id] = (x, y, w, h)
                self.next_id += 1
        
        # إزالة الكائنات القديمة
        self._cleanup_old_objects(current_frame)
        
        return current_frame
    
    def _cleanup_old_objects(self, current_frame: dict):
        """إزالة الكائنات التي لم تعد مكتشفة"""
        to_remove = []
        for obj_id in self.tracked_objects:
            if obj_id not in current_frame:
                to_remove.append(obj_id)
        
        for obj_id in to_remove:
            del self.tracked_objects[obj_id]
    
    def get_trajectory(self, obj_id: int) -> List[Tuple[int, int]]:
        """الحصول على مسار الكائن"""
        return self.tracked_objects.get(obj_id, [])
    
    def get_velocity(self, obj_id: int) -> Tuple[float, float]:
        """حساب سرعة الكائن"""
        trajectory = self.get_trajectory(obj_id)
        if len(trajectory) < 2:
            return (0.0, 0.0)
        
        # حساب متوسط السرعة على آخر 3 إطارات
        recent_points = trajectory[-3:]
        if len(recent_points) < 2:
            return (0.0, 0.0)
        
        dx = recent_points[-1][0] - recent_points[0][0]
        dy = recent_points[-1][1] - recent_points[0][1]
        dt = len(recent_points) - 1
        
        return (dx / dt, dy / dt)

class ColorAnalyzer:
    """محلل الألوان للكائنات المكتشفة"""
    
    @staticmethod
    def get_dominant_color(image: np.ndarray, x: int, y: int, 
                          width: int, height: int) -> Tuple[int, int, int]:
        """الحصول على اللون السائد في منطقة الكائن"""
        # استخراج المنطقة
        roi = image[y:y+height, x:x+width]
        
        if roi.size == 0:
            return (0, 0, 0)
        
        # تحويل إلى BGR
        if len(roi.shape) == 3 and roi.shape[2] == 3:
            roi_bgr = roi
        else:
            roi_bgr = cv2.cvtColor(roi, cv2.COLOR_GRAY2BGR)
        
        # حساب متوسط اللون
        mean_color = cv2.mean(roi_bgr)[:3]
        return tuple(map(int, mean_color))
    
    @staticmethod
    def classify_color(bgr_color: Tuple[int, int, int]) -> str:
        """تصنيف اللون إلى اسم"""
        b, g, r = bgr_color
        
        # تحويل إلى HSV لتصنيف أفضل
        hsv = cv2.cvtColor(np.uint8([[[b, g, r]]]), cv2.COLOR_BGR2HSV)[0][0]
        h, s, v = hsv
        
        if v < 50:
            return "أسود"
        elif v > 200 and s < 50:
            return "أبيض"
        elif s < 50:
            return "رمادي"
        elif h < 10 or h > 170:
            return "أحمر"
        elif 10 <= h < 25:
            return "برتقالي"
        elif 25 <= h < 35:
            return "أصفر"
        elif 35 <= h < 85:
            return "أخضر"
        elif 85 <= h < 130:
            return "أزرق"
        elif 130 <= h < 170:
            return "بنفسجي"
        else:
            return "غير محدد"

def create_sample_image_with_objects():
    """إنشاء صورة تجريبية مع كائنات ملونة للاختبار"""
    # إنشاء صورة بيضاء
    image = np.ones((480, 640, 3), dtype=np.uint8) * 255
    
    # رسم مستطيلات ملونة
    colors = [
        ((255, 0, 0), "أزرق"),      # BGR
        ((0, 255, 0), "أخضر"),
        ((0, 0, 255), "أحمر"),
        ((255, 255, 0), "سماوي"),
        ((255, 0, 255), "وردي"),
        ((0, 255, 255), "أصفر")
    ]
    
    for i, ((b, g, r), name) in enumerate(colors):
        x = 50 + (i % 3) * 180
        y = 100 + (i // 3) * 150
        
        cv2.rectangle(image, (x, y), (x + 120, y + 80), (b, g, r), -1)
        cv2.putText(image, name, (x + 10, y + 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    return image

if __name__ == "__main__":
    print("🛠️ أدوات HUSKYLENS المساعدة")
    print("📊 إنشاء صورة تجريبية...")
    
    # إنشاء صورة تجريبية
    test_image = create_sample_image_with_objects()
    
    # حفظ الصورة
    cv2.imwrite("test_image.jpg", test_image)
    print("✅ تم إنشاء صورة تجريبية: test_image.jpg")
    
    # اختبار محلل الألوان
    analyzer = ColorAnalyzer()
    
    # تحليل لون المستطيل الأول
    dominant_color = analyzer.get_dominant_color(test_image, 50, 100, 120, 80)
    color_name = analyzer.classify_color(dominant_color)
    
    print(f"🎨 اللون السائد: {dominant_color} - {color_name}")
    
    print("✅ انتهاء اختبار الأدوات المساعدة")
