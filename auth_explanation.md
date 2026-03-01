# Auth.py Line-by-Line & Word-by-Word Explanation (Thanglish)

Indha document-la `backend/crowd_fund_api/app/core/auth.py` file-oda ovvoru line-um, andha line-la iruka ovvoru word-um enna pannudhu-nu clear-ah explain panni iruken.

---

## 1. Imports Section (Lines 1-8)

### **Line 1: `from datetime import datetime, timedelta`**
*   **from**: Oru particular library-la irundhu.
*   **datetime**: Date and Time details handle panna use aagura main module.
*   **import**: Namaku thevayana functions-ah eduthukuroam.
*   **datetime (2nd time)**: Current time, date-ah eduka use aagum.
*   **timedelta**: Time difference (e.g., 30 mins, 1 day) calculate panna use aagum.
*   **Meaning**: Token eppo expire aaganum-nu time calculate panna indha library use aagudhu.

### **Line 2: `from typing import Optional`**
*   **typing**: Variable types-ah define panna use aagura module.
*   **Optional**: Oru data kandippa irukanum-nu avasiyam illai (andha data `None`-ah kuda irukalam) appadinu solrathuku.
*   **Meaning**: Function arguments oru vela kudukalana kuda adhu handle panna use aagudhu.

### **Line 3: `from jose import JWTError, jwt`**
*   **jose**: JavaScript Object Signing and Encryption library. Tokens create panna use aagudhu.
*   **JWTError**: Token decoding pannum bodhu edhavadhu error vandha handle panna.
*   **jwt**: JSON Web Token create/decode panna main tool.
*   **Meaning**: User identity-ah protect panna use aagura JWT tokens-ah manage panna indha library thevai.

### **Line 4: `from fastapi import Depends, HTTPException, status`**
*   **fastapi**: Inga use panra main web framework.
*   **Depends**: Dependency Injection. Oru function kulla innoru function result-ah ready-ah eduthu veika.
*   **HTTPException**: Server-la error errors (like 401 Unauthorized) send panna.
*   **status**: HTTP status codes (200, 401, 404, etc.) easy-ah use panna.
*   **Meaning**: FastAPI features-ah login and security-ku connect panna use aagudhu.

### **Line 5: `from fastapi.security import OAuth2PasswordBearer`**
*   **OAuth2PasswordBearer**: Security standard flow. Token-ah request header-la irundhu automatic-ah edukum.
*   **Meaning**: User login panna apram header-la vara token-ah find panna indha tool help pannum.

### **Line 6: `from sqlalchemy.orm import Session`**
*   **sqlalchemy.orm**: Database connection-ah objects-ah handle panna.
*   **Session**: Database-kuda pesura oru active connection "talk".
*   **Meaning**: DB query panna indha type thevai.

### **Line 7: `from app.database import get_db`**
*   **app.database**: Namma project-la iruka DB config file.
*   **get_db**: Database connection-ah start panni thara function.
*   **Meaning**: DB connection-ah indha file-ku kondu varoam.

### **Line 8: `from app.models.user_model import User`**
*   **app.models.user_model**: User table-oda structure iruka file.
*   **User**: Database-la iruka 'User' table model.
*   **Meaning**: Login panra user DB-la irukara-nu check panna indha model thevai.
---

## 2. Configuration Section (Lines 10-15)

### **Line 10: `import bcrypt`**
*   **import**: Library-ah load panroam.
*   **bcrypt**: Password-ah encrypt (hash) panna powerful tool. Security-ku romba mukkiyam.

### **Line 13: `SECRET_KEY = "your_secret_key_here"`**
*   **SECRET_KEY**: Token generate pannum bodhu use aagura oru secret password. Idhu yarukum theriya kudathu.
*   **Meaning**: Indha key vechu dhan tokens genuine-ah-nu check pannuvom.

### **Line 14: `ALGORITHM = "HS256"`**
*   **ALGORITHM**: Token-ah encode panna use panra mathematical method. 256-bit hashing idhu.

### **Line 15: `ACCESS_TOKEN_EXPIRE_MINUTES = 30`**
*   **ACCESS_TOKEN_EXPIRE_MINUTES**: Token evlo neram valid-ah irukanum? Inga 30 nimidangal set panni irukoam.

---

## 3. Password Security Functions (Lines 18-40)

### **Line 18: `oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")`**
*   **oauth2_scheme**: Variable name.
*   **tokenUrl**: Token enga irundhu varum-nu URL soldroam (Login endpoint).
*   **Meaning**: Client login pannum bodhu eppa token header-la varu-nu identify panna idhu setup.

### **Line 20: `def verify_password(plain_password: str, hashed_password: str):`**
*   **def**: Function-ah create panroam.
*   **verify_password**: Function name.
*   **plain_password**: User type panna normal password.
*   **hashed_password**: DB-la already safe-ah store aagi iruka encrypted password.

### **Lines 21-31: Password Verification Logic**
*   **try...except**: Code-la edhavadhu unexpected error vandha crash aagama handle panna.
*   **pw_bytes = plain_password.encode('utf-8')**: Normal text password-ah bytes data-va mathurom (bcrypt bytes dhan use pannum).
*   **if len(pw_bytes) > 72**: Bcrypt-la 72 chars mela hash panna mudiyadhu.
*   **pw_bytes = pw_bytes[:72]**: Length athigama irundha 72 mark-oada cut (truncate) panroam.
*   **bcrypt.checkpw(...)**: Indha function dhan main magic! Plain password-um DB-la iruka hashed password-um match aagudha-nu check pannum. True or False tharum.

### **Line 33: `def get_password_hash(password: str):`**
*   **Meaning**: User register pannum bodhu, avanga password-ah safe-ah mathurom (Hash function).

### **Lines 35-40: Hashing Logic**
*   **salt = bcrypt.gensalt()`**: Oru random string (Salt) create pannum. Idhu password-ah innum secure-ah mathum.
*   **bcrypt.hashpw(...)**: Password + Salt rendayum serthu oru unreadable code-ah (Hash) mathum.
*   **decode('utf-8')**: Byte data-va thirumbayum string form-ku mathi return pannum.

---

## 4. Token Creation (Lines 42-50)

### **Line 42: `def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):`**
*   **data**: Token-ulla enna info irukanum (like user_id, email).
*   **expires_delta**: Token expiry time extra-va set panna oru optional argument.

### **Line 43: `to_encode = data.copy()`**
*   **copy()**: Original data-va mathama, oru copy eduthu adhu mela token expiry details sethu pathukkuroam.

### **Lines 44-48: Expiry Management**
*   **datetime.utcnow()**: Adha second-la iruka standard (UTC) time.
*   **timedelta(minutes=...)**: Eppo expire aaganum-nu andha time-ah add panroam.
*   **to_encode.update({"exp": expire})**: Token data-kulla expiry time-ah add panroam.

### **Line 49: `encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)`**
*   **jwt.encode**: User data + Secret Key + Algorithm ellathayum serthu oru long string-ah (JWT Token) generate pannum.
*   **Meaning**: Indha string dhan client-ku (frontend) response-ah pogum.

---

## 5. Get Current User (Security Dependency) (Lines 52-70)

### **Line 52: `def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):`**
*   **get_current_user**: Yaru ippa login panni iruka? nu find panna indha function.
*   **Depends(oauth2_scheme)**: Automatic-ah header-la irundhu token-ah edukum.
*   **Depends(get_db)**: DB connection-ah input-ah kondu varum.

### **Lines 53-57: Exception Setup**
*   **credentials_exception**: Token thappa irundha, expire aagi irundha, or yaro hack panna try panna, 401 Unauthorized error-ah return panna idhu error template.

### **Lines 58-64: Token Decoding**
*   **jwt.decode(...)**: Frontend-la irundhu vandha "encoded string"-ah thirumbayum readable data-va mathuradhu.
*   **payload.get("sub")**: "sub" (Subject) field-la dhan namma Phone Number or ID vechu irupom. Adha edukuroam.
*   **raise credentials_exception**: Edhavadhu data mis-match aana error kaaturom.

### **Line 67: `user = db.query(User).filter(User.phone_number == phone_number).first()`**
*   **db.query(User)**: Database-la "User" table-la search panroam.
*   **filter**: Mobile number match aagura user-ah mattum edukurom.
*   **first()**: First matching user-ah mattum edukurom.

### **Line 70: `return user`**
*   **Meaning**: User identity confirm aagiduchu, ippa indha "User" object-ah backend logic-ku use panna anupuroam.

---

Idhu dhan **auth.py** file-oda full explanation. Idhula hashing (security), tokens (identity), and DB checks (validation) pathi clear-ah iruku.
