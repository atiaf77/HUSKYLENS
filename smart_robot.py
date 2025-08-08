"""
روبوت ذكي باستخدام HUSKYLENS
Smart Robot using HUSKYLENS

مثال لروبوت يتبع الوجوه والكائنات
"""

from huskylens import HuskyLens, HuskyLensObject
import time
import threading
from typing import List, Optional

class SmartRobot:
    """روبوت ذكي مع HUSKYLENS"""
    
    def __init__(self, huskylens_port: str = 'COM3'):
        self.husky = HuskyLens(huskylens_port)
        self.is_running = False
        self.current_target: Optional[HuskyLensObject] = None
        self.mode = "idle"  # idle, face_tracking, object_tracking, color_tracking
        
    def start(self) -> bool:
        """بدء تشغيل الروبوت"""
        if self.husky.connect():
            self.is_running = True
            print("🤖 الروبوت الذكي جاهز للعمل!")
            return True
        else:
            print("❌ فشل في تشغيل الروبوت - تحقق من اتصال HUSKYLENS")
            return False
    
    def stop(self):
        """إيقاف الروبوت"""
        self.is_running = False
        self.husky.disconnect()
        print("🛑 تم إيقاف الروبوت")
    
    def set_face_tracking_mode(self):
        """تعيين وضع تتبع الوجوه"""
        self.mode = "face_tracking"
        self.husky.set_algorithm(HuskyLens.FACE_RECOGNITION)
        print("👤 الروبوت في وضع تتبع الوجوه")
    
    def set_object_tracking_mode(self):
        """تعيين وضع تتبع الكائنات"""
        self.mode = "object_tracking"
        self.husky.set_algorithm(HuskyLens.OBJECT_TRACKING)
        print("📦 الروبوت في وضع تتبع الكائنات")
    
    def set_color_tracking_mode(self, learn_new_color: bool = True):
        """تعيين وضع تتبع الألوان"""
        self.mode = "color_tracking"
        self.husky.set_algorithm(HuskyLens.COLOR_RECOGNITION)
        
        if learn_new_color:
            print("🎨 ضع كائناً ملوناً أمام الكاميرا...")
            input("اضغط Enter لتعليم اللون...")
            self.husky.learn_object(1)
            print("✅ تم تعلم اللون!")
        
        print("🎨 الروبوت في وضع تتبع الألوان")
    
    def get_detections(self) -> List[HuskyLensObject]:
        """الحصول على الكائنات المكتشفة"""
        if not self.is_running:
            return []
        
        return self.husky.get_blocks()
    
    def find_best_target(self, detections: List[HuskyLensObject]) -> Optional[HuskyLensObject]:
        """العثور على أفضل هدف للتتبع"""
        if not detections:
            return None
        
        # اختيار أكبر كائن (الأقرب غالباً)
        best_target = max(detections, key=lambda obj: obj.width * obj.height)
        return best_target
    
    def calculate_movement_direction(self, target: HuskyLensObject) -> str:
        """حساب اتجاه الحركة المطلوب"""
        center_x = target.center_x
        center_y = target.center_y
        
        # افتراض أن عرض الشاشة 320 وارتفاعها 240
        screen_width = 320
        screen_height = 240
        
        # مناطق التحكم
        left_zone = screen_width // 3
        right_zone = 2 * screen_width // 3
        top_zone = screen_height // 3
        bottom_zone = 2 * screen_height // 3
        
        movements = []
        
        # الاتجاه الأفقي
        if center_x < left_zone:
            movements.append("يسار")
        elif center_x > right_zone:
            movements.append("يمين")
        else:
            movements.append("توقف_أفقي")
        
        # الاتجاه العمودي (للكاميرا المتحركة)
        if center_y < top_zone:
            movements.append("أعلى")
        elif center_y > bottom_zone:
            movements.append("أسفل")
        else:
            movements.append("توقف_عمودي")
        
        # تحديد قرب/بعد الكائن بناءً على الحجم
        object_size = target.width * target.height
        if object_size < 2000:  # كائن صغير = بعيد
            movements.append("تقدم")
        elif object_size > 8000:  # كائن كبير = قريب
            movements.append("تراجع")
        else:
            movements.append("توقف_عمق")
        
        return " + ".join(movements)
    
    def execute_movement(self, direction: str):
        """تنفيذ الحركة (محاكاة - يمكن ربطها بمحركات حقيقية)"""
        print(f"🚀 تنفيذ الحركة: {direction}")
        
        # هنا يمكن إضافة كود التحكم الفعلي في المحركات
        # مثل Arduino, Raspberry Pi, إلخ
        
        if "يسار" in direction:
            self.move_left()
        if "يمين" in direction:
            self.move_right()
        if "تقدم" in direction:
            self.move_forward()
        if "تراجع" in direction:
            self.move_backward()
        if "أعلى" in direction:
            self.camera_up()
        if "أسفل" in direction:
            self.camera_down()
    
    def move_left(self):
        """حركة يسار"""
        print("⬅️ تحرك يساراً")
        # كود التحكم في المحرك الأيسر هنا
    
    def move_right(self):
        """حركة يمين"""
        print("➡️ تحرك يميناً")
        # كود التحكم في المحرك الأيمن هنا
    
    def move_forward(self):
        """حركة للأمام"""
        print("⬆️ تحرك للأمام")
        # كود التحكم في المحركات للأمام هنا
    
    def move_backward(self):
        """حركة للخلف"""
        print("⬇️ تحرك للخلف")
        # كود التحكم في المحركات للخلف هنا
    
    def camera_up(self):
        """توجيه الكاميرا للأعلى"""
        print("📹⬆️ توجيه الكاميرا للأعلى")
        # كود التحكم في محرك الكاميرا هنا
    
    def camera_down(self):
        """توجيه الكاميرا للأسفل"""
        print("📹⬇️ توجيه الكاميرا للأسفل")
        # كود التحكم في محرك الكاميرا هنا
    
    def run_tracking_loop(self):
        """حلقة التتبع الرئيسية"""
        print(f"🔄 بدء حلقة التتبع في وضع: {self.mode}")
        
        no_target_count = 0
        max_no_target = 10  # عدد المحاولات قبل التوقف
        
        while self.is_running:
            try:
                # الحصول على الكائنات المكتشفة
                detections = self.get_detections()
                
                if detections:
                    # إعادة تعيين العداد
                    no_target_count = 0
                    
                    # العثور على أفضل هدف
                    target = self.find_best_target(detections)
                    self.current_target = target
                    
                    # حساب الاتجاه المطلوب
                    direction = self.calculate_movement_direction(target)
                    
                    # تنفيذ الحركة
                    self.execute_movement(direction)
                    
                    # عرض معلومات الهدف
                    print(f"🎯 الهدف: موقع({target.center_x}, {target.center_y}), حجم: {target.width}x{target.height}")
                
                else:
                    # لا يوجد هدف
                    no_target_count += 1
                    self.current_target = None
                    
                    if no_target_count <= max_no_target:
                        print(f"🔍 البحث عن هدف... ({no_target_count}/{max_no_target})")
                        # دوران بحث
                        self.search_rotation()
                    else:
                        print("😴 توقف - لا يوجد هدف")
                        self.stop_all_movement()
                
                # انتظار قبل القراءة التالية
                time.sleep(0.1)  # 10 FPS
                
            except Exception as e:
                print(f"❌ خطأ في حلقة التتبع: {e}")
                time.sleep(1)
    
    def search_rotation(self):
        """دوران بحث عن الهدف"""
        print("🔄 دوران بحث...")
        # كود الدوران البطيء للبحث
    
    def stop_all_movement(self):
        """إيقاف جميع الحركات"""
        print("🛑 إيقاف جميع الحركات")
        # كود إيقاف المحركات

def interactive_robot_demo():
    """عرض تفاعلي للروبوت الذكي"""
    print("🤖 مرحباً بك في الروبوت الذكي!")
    print("=" * 40)
    
    # إنشاء الروبوت
    robot = SmartRobot('COM3')  # غير المنفذ حسب نظامك
    
    if not robot.start():
        return
    
    try:
        while True:
            print("\n🎯 اختر وضع التشغيل:")
            print("1️⃣  تتبع الوجوه")
            print("2️⃣  تتبع الكائنات")
            print("3️⃣  تتبع الألوان")
            print("4️⃣  وضع الخمول (إيقاف التتبع)")
            print("0️⃣  إيقاف الروبوت")
            
            choice = input("\n👉 اختيارك: ").strip()
            
            if choice == '1':
                robot.set_face_tracking_mode()
                print("▶️ اضغط Ctrl+C لإيقاف التتبع")
                robot.run_tracking_loop()
                
            elif choice == '2':
                robot.set_object_tracking_mode()
                print("▶️ اضغط Ctrl+C لإيقاف التتبع")
                robot.run_tracking_loop()
                
            elif choice == '3':
                robot.set_color_tracking_mode()
                print("▶️ اضغط Ctrl+C لإيقاف التتبع")
                robot.run_tracking_loop()
                
            elif choice == '4':
                robot.mode = "idle"
                print("😴 الروبوت في وضع الخمول")
                
            elif choice == '0':
                break
                
            else:
                print("❌ اختيار غير صحيح")
    
    except KeyboardInterrupt:
        print("\n⏸️ تم إيقاف التتبع بواسطة المستخدم")
    
    finally:
        robot.stop()

if __name__ == "__main__":
    print("🤖 الروبوت الذكي مع HUSKYLENS")
    print("🔧 تأكد من توصيل HUSKYLENS قبل البدء")
    print("⚠️ هذا مثال محاكاة - يمكن ربطه بمحركات حقيقية")
    print()
    
    interactive_robot_demo()
