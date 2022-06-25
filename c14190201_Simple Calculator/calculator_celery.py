from celery import Celery

app = Celery('calculator', broker='pyamqp://guest:guest@localhost:5672', backend=f'redis://localhost:6379')

@app.task
def bil_palindrom_prima(idx):
    prima = 0
    hasil = 0
    ctr = 2

    while prima != idx:
        factor = 0
        for i in range(1, ctr + 1):
            if ctr % i == 0:
                factor += 1  
        reverse = 0
        tmp = ctr
        while tmp != 0:
            left = tmp % 10
            reverse = reverse * 10 + left
            tmp = int(tmp / 10)

        if factor == 2 and reverse == ctr:
            prima += 1
            hasil = ctr

        ctr  += 1

    return hasil

@app.task
def bil_prima(idx):
    prima = 0
    hasil = 0
    ctr = 2
    while prima != idx:
        factor = 0
        for i in range(1, ctr + 1):
            if ctr % i == 0:
                factor += 1

        if factor == 2:
            prima += 1
            hasil = ctr
        ctr  += 1

    return hasil
