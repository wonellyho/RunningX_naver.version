const express = require('express');
const app = express();

app.use(express.json());

// POST 요청 핸들러
app.post('/submit-location', (req, res) => {
    const { latitude, longitude } = req.body;
    console.log(`받은 위치: 위도=${latitude}, 경도=${longitude}`);
    res.json({ message: '위치 데이터 수신 완료' });
});

// GET 요청 핸들러 (추가)
app.get('/', (req, res) => {
    res.send('서버가 실행 중입니다. POST 요청으로 /submit-location 경로에 위치 데이터를 보내세요.');
});

// 서버 실행
app.listen(3000, () => console.log('서버 실행 중...'));
