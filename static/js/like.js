const API_LIKES_BASE = "/api/likes";

async function fetchLikes() {
    try {
        const res = await fetch(`${API_LIKES_BASE}/${POST_ID}`);
        const data = await res.json();
        document.getElementById('count').innerText = data.count || 0;
    } catch (e) { console.error("いいね数取得失敗"); }
}

async function doLike() {
    try {
        const res = await fetch(`${API_LIKES_BASE}/${POST_ID}`, { method: 'POST' });
        const data = await res.json();
        if (data.status === 'ok') {
            document.getElementById('count').innerText = data.count;
        } else {
            alert(data.message);
        }
    } catch (e) { alert("通信エラー"); }
}

fetchLikes();