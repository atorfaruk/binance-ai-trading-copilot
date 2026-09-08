from app.scoring import sma,calculate_features,setup_score
def test_sma(): assert sma([1,2,3,4],2)==3.5
def test_score_bounded():
    c=[100+i for i in range(30)]; v=[1000+i*10 for i in range(30)]
    f=calculate_features(c,v); assert 0<=setup_score(f)<=100; assert f.ema_fast>f.ema_slow
