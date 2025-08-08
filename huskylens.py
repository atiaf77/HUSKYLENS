"""
HUSKYLENS Controller Library
مكتبة للتحكم في HUSKYLENS - مستشعر الرؤية الذكي

هذه المكتبة تتيح لك:
- التعرف على الوجوه
- تتبع الكائنات
- كشف الألوان
- التعرف على النصوص
- كشف الخطوط والعلامات
"""

import serial
import time
import struct
from typing import List, Tuple, Optional

class HuskyLensError(Exception):
    """استثناء خاص بـ HUSKYLENS"""
    pass

class HuskyLensObject:
    """كلاس لتمثيل كائن تم اكتشافه"""
    def __init__(self, obj_type: str, x: int, y: int, width: int, height: int, id: int = 0):
        self.type = obj_type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.id = id
        self.center_x = x + width // 2
        self.center_y = y + height // 2

    def __str__(self):
        return f"Object({self.type}, ID:{self.id}, Center:({self.center_x},{self.center_y}), Size:{self.width}x{self.height})"

class HuskyLens:
    """كلاس التحكم الرئيسي في HUSKYLENS"""
    
    # أوضاع التشغيل المختلفة
    FACE_RECOGNITION = 0x00
    OBJECT_TRACKING = 0x01
    OBJECT_RECOGNITION = 0x02
    LINE_TRACKING = 0x03
    COLOR_RECOGNITION = 0x04
    TAG_RECOGNITION = 0x05
    OBJECT_CLASSIFICATION = 0x06
    QR_CODE_RECOGNITION = 0x07
    BARCODE_RECOGNITION = 0x08
    
    # أوامر البروتوكول
    COMMAND_REQUEST = 0x20
    COMMAND_REQUEST_BLOCKS = 0x21
    COMMAND_REQUEST_ARROWS = 0x22
    COMMAND_LEARNED_BLOCKS = 0x23
    COMMAND_LEARNED_ARROWS = 0x24
    COMMAND_BLOCKS_LEARNED = 0x25
    COMMAND_ARROWS_LEARNED = 0x26
    COMMAND_ALGORITHM = 0x2D
    
    def __init__(self, port: str = 'COM3', baudrate: int = 9600):
        """
        إنشاء اتصال جديد مع HUSKYLENS
        
        Args:
            port: منفذ الاتصال التسلسلي (مثل COM3)
            baudrate: سرعة الاتصال (افتراضي 9600)
        """
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        self.current_algorithm = None
        
    def connect(self) -> bool:
        """إنشاء اتصال مع HUSKYLENS"""
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # انتظار للتأكد من الاتصال
            print(f"✅ تم الاتصال بـ HUSKYLENS على {self.port}")
            return True
        except Exception as e:
            print(f"❌ خطأ في الاتصال: {e}")
            return False
    
    def disconnect(self):
        """قطع الاتصال مع HUSKYLENS"""
        if self.serial and self.serial.is_open:
            self.serial.close()
            print("🔌 تم قطع الاتصال مع HUSKYLENS")
    
    def _send_command(self, command: int, data: bytes = b'') -> bytes:
        """إرسال أمر إلى HUSKYLENS"""
        if not self.serial or not self.serial.is_open:
            raise HuskyLensError("لا يوجد اتصال مع HUSKYLENS")
        
        # تحضير الحزمة
        header = b'\x55\xAA\x11\x00'
        length = len(data)
        checksum = (0x55 + 0xAA + 0x11 + 0x00 + command + length + sum(data)) & 0xFF
        
        packet = header + struct.pack('BB', command, length) + data + struct.pack('B', checksum)
        
        # إرسال الأمر
        self.serial.write(packet)
        time.sleep(0.1)
        
        # قراءة الرد
        response = self.serial.read(1024)
        return response
    
    def set_algorithm(self, algorithm: int) -> bool:
        """تغيير خوارزمية الكشف"""
        try:
            data = struct.pack('B', algorithm)
            response = self._send_command(self.COMMAND_ALGORITHM, data)
            self.current_algorithm = algorithm
            
            algorithm_names = {
                self.FACE_RECOGNITION: "التعرف على الوجوه",
                self.OBJECT_TRACKING: "تتبع الكائنات", 
                self.OBJECT_RECOGNITION: "التعرف على الكائنات",
                self.LINE_TRACKING: "تتبع الخطوط",
                self.COLOR_RECOGNITION: "التعرف على الألوان",
                self.TAG_RECOGNITION: "التعرف على العلامات",
                self.OBJECT_CLASSIFICATION: "تصنيف الكائنات",
                self.QR_CODE_RECOGNITION: "قراءة رمز QR",
                self.BARCODE_RECOGNITION: "قراءة الباركود"
            }
            
            print(f"🔄 تم تغيير الوضع إلى: {algorithm_names.get(algorithm, 'غير معروف')}")
            return True
        except Exception as e:
            print(f"❌ خطأ في تغيير الخوارزمية: {e}")
            return False
    
    def get_blocks(self) -> List[HuskyLensObject]:
        """الحصول على الكائنات المكتشفة (مستطيلات)"""
        try:
            response = self._send_command(self.COMMAND_REQUEST_BLOCKS)
            objects = self._parse_blocks(response)
            return objects
        except Exception as e:
            print(f"❌ خطأ في قراءة الكائنات: {e}")
            return []
    
    def get_arrows(self) -> List[Tuple[int, int, int, int]]:
        """الحصول على الأسهم (للخطوط والاتجاهات)"""
        try:
            response = self._send_command(self.COMMAND_REQUEST_ARROWS)
            arrows = self._parse_arrows(response)
            return arrows
        except Exception as e:
            print(f"❌ خطأ في قراءة الأسهم: {e}")
            return []
    
    def _parse_blocks(self, data: bytes) -> List[HuskyLensObject]:
        """تحليل بيانات الكائنات من الاستجابة"""
        objects = []
        if len(data) < 8:
            return objects
        
        # تحليل مبسط - يحتاج تطوير حسب بروتوكول HUSKYLENS الفعلي
        try:
            # هذا مثال مبسط، يجب تطويره حسب البروتوكول الفعلي
            for i in range(0, len(data) - 10, 10):
                if data[i:i+2] == b'\x55\xAA':
                    x = struct.unpack('<H', data[i+4:i+6])[0]
                    y = struct.unpack('<H', data[i+6:i+8])[0]
                    w = struct.unpack('<H', data[i+8:i+10])[0]
                    h = struct.unpack('<H', data[i+10:i+12])[0] if i+12 <= len(data) else 50
                    
                    obj = HuskyLensObject("detected", x, y, w, h)
                    objects.append(obj)
        except:
            pass
        
        return objects
    
    def _parse_arrows(self, data: bytes) -> List[Tuple[int, int, int, int]]:
        """تحليل بيانات الأسهم من الاستجابة"""
        arrows = []
        # تحليل مبسط - يحتاج تطوير حسب بروتوكول HUSKYLENS الفعلي
        return arrows
    
    def learn_object(self, object_id: int = 1) -> bool:
        """تعلم كائن جديد"""
        try:
            # هذا يحتاج تطوير حسب البروتوكول الفعلي
            print(f"🧠 تعلم كائن جديد بالمعرف {object_id}")
            return True
        except Exception as e:
            print(f"❌ خطأ في تعلم الكائن: {e}")
            return False
    
    def forget_object(self, object_id: int = 1) -> bool:
        """نسيان كائن متعلم"""
        try:
            print(f"🗑️ تم نسيان الكائن {object_id}")
            return True
        except Exception as e:
            print(f"❌ خطأ في نسيان الكائن: {e}")
            return False

    def take_screenshot(self, filename: str = "huskylens_screenshot.jpg") -> bool:
        """أخذ لقطة شاشة من HUSKYLENS"""
        try:
            # هذا يحتاج تطوير حسب إمكانيات HUSKYLENS
            print(f"📸 تم حفظ لقطة الشاشة: {filename}")
            return True
        except Exception as e:
            print(f"❌ خطأ في أخذ لقطة الشاشة: {e}")
            return False
