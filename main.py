def patch_data(var):
    try:
        if var == 'bio':
            firebase.get("classification/biodegradable", "bio")
            bio_count = firebase.bio
            firebase.patch("classification", {"biodegradable": bio_count+1}, bg=0)
        elif var == 'nonbio':
            firebase.get("classification/non-biodegradable", "nonbio")
            nonbio_count = firebase.nonbio
            firebase.patch("classification", {"non-biodegradable": nonbio_count+1}, bg=0)
        elif var == 'recyc':
            firebase.get("classification/recyclable", "recyc")
            recyc_count = firebase.recyc
            firebase.patch("classification", {"recyclable": recyc_count+1}, bg=0)
        else:
            pass
        time.sleep_ms(50)
    except:
        pass

def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def degrees(angle, minm, maxm):
    return map(angle, 0, 180, minm, maxm)

def bio_servo():
    led.off()
    minm, maxm, = 42, 140
    pwm1.duty(degrees(0, minm, maxm))
    time.sleep(2)
    pwm1.duty(degrees(115, minm, maxm))
    patch_data('bio')
    led.on()
    
def nonbio_servo():
    led.off()
    minm, maxm = 20, 123
    pwm2.duty(degrees(0, minm, maxm))
    time.sleep(2)
    pwm2.duty(degrees(115, minm, maxm))
    patch_data('nonbio')
    led.on()

def recyc_servo():
    led.off()
    minm, maxm = 24, 125
    pwm3.duty(degrees(0, minm, maxm))
    time.sleep(2)
    pwm3.duty(degrees(115, minm, maxm))
    patch_data('recyc')
    led.on()
    
while True:
    if uart.any():
        data = uart.read(1).decode('utf-8')
        
        if data == 'b': #BIO
            bio_servo()
            uart.read() # to clear bytes in buffer
        elif data == 'n': #NONBIO
            nonbio_servo()
            uart.read()
        elif data == 'r': #RECYCLABLE
            recyc_servo()
            uart.read()
        else:
            pass
