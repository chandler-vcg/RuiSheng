<template>
  <div class="loginVideo">
    <div class="loginBox">
      <!-- 登录框 -->
      <div class="container">
        <div class="drop">
          <div class="content">
            <h2 :style="{ color: '#55557f' }">睿声</h2>
            <form>
              <div class="inputBox">
                <input type="text" placeholder="用户名" />
              </div>
              <div class="inputBox">
                <input type="password" placeholder="密码" />
              </div>
              <div class="buttonGroup">
                <div class="inputBox loginBtn">
                  <span @click="degnlu">登录</span>
                </div>
                <div class="inputBox registerBtn">
                  <span @click="zhuce">注册</span>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
const router = useRouter();

const degnlu = async () => {
  uni.navigateTo({
    url:"/pages/index/explaination"
  })
}

const zhuce = async () => {
  uni.navigateTo({
    url:"/pages/index/explaination"
  })
}
</script>

<style scoped>
.loginVideo {
  width: 100%;
  height: 100vh;
  overflow: hidden;
  position: relative;
  background: url('/static/bk.png');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
}

.loginBox {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.container .drop {
  position: relative;
  width: 350px;
  height: 350px;
  box-shadow: inset 20px 20px 20px rgba(0, 0, 0, 0.05),
    25px 35px 20px rgba(0, 0, 0, 0.05), 25px 30px 30px rgba(0, 0, 0, 0.05),
    inset -20px -20px 25px rgba(255, 255, 255, 0.9);
  transition: 0.5s;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
}

.container .drop:hover {
  border-radius: 10%;
}

.container .drop::before {
  content: "";
  position: absolute;
  top: 50px;
  left: 85px;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  background: #fff;
  opacity: 0.9;
}

.container .drop::after {
  content: "";
  position: absolute;
  top: 90px;
  left: 110px;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  background: #fff;
  opacity: 0.9;
}

.container .drop .content {
  position: relative;
  display: flex;
  justify-content: center;
  flex-direction: column;
  text-align: center;
  padding: 40px;
  gap: 15px;
}

.container .drop .content h2 {
  position: relative;
  color: #333;
  font-size: 1.5em;
}

.container .drop .content form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.container .drop .content form .inputBox {
  margin-top: 10px;
  position: relative;
  width: 225px;
  box-shadow: inset 2px 5px 10px rgba(0, 0, 0, 0.1),
    inset -2px -5px 10px rgba(255, 255, 255, 1),
    15px 15px 10px rgba(0, 0, 0, 0.05), 15px 10px 15px rgba(0, 0, 0, 0.025);
  border-radius: 25px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.container .drop .content form .inputBox::before {
  content: "";
  position: absolute;
  top: 8px;
  left: 50%;
  transform: translateX(-50%);
  width: 65%;
  height: 5px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 5px;
}

.container .drop .content form .inputBox input {
  border: none;
  outline: none;
  background: transparent;
  width: 100%;
  font-size: 1em;
  padding: 10px 15px;
}

/* 按钮组样式 */
.buttonGroup {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-top: 20px;
  width: 200px;
  margin-left: 15px;
}

/* 登录注册按钮容器 */
.inputBox.loginBtn,
.inputBox.registerBtn {
  width: 100px;
  border-radius: 25px;
  transition: all 0.3s;
  cursor: pointer;
}

/* 按钮文本样式 */
.inputBox.loginBtn span,
.inputBox.registerBtn span {
  display: block;
  width: 100%;
  padding: 12px;
  color: white;
  text-align: center;
  font-size: 1em;
  letter-spacing: 1px;
  user-select: none;
}

/* 登录按钮配色 */
.inputBox.loginBtn {
  background: #3399ff;
  box-shadow: inset 2px 5px 10px rgba(0, 0, 0, 0.1),
    15px 15px 10px rgba(0, 0, 0, 0.05),
    15px 10px 15px rgba(0, 0, 0, 0.025);
}

.inputBox.loginBtn:hover {
  width: 120px;
  background: #297acc;
}

/* 注册按钮配色 */
.inputBox.registerBtn {
  background: #00a6bc;
  box-shadow: inset 2px 5px 10px rgba(0, 0, 0, 0.1),
    15px 15px 10px rgba(0, 0, 0, 0.05),
    15px 10px 15px rgba(0, 0, 0, 0.025);
}

.inputBox.registerBtn:hover {
  width: 120px;
  background: #008999;
}

/* 保持原有悬停动画 */
.container .drop .content form .inputBox:last-child:hover {
}

.btns {
  /* 保持原有附加按钮样式 */ 
  position: absolute;
  right: -120px;
  bottom: 0;
  width: 120px;
  height: 120px;
  background: #00a6bc;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  text-decoration: none;
  color: #fff;
  line-height: 1.2em;
  letter-spacing: 0.1em;
  font-size: 0.8em;
  transition: 0.25s;
  text-align: center;
  box-shadow: inset 10px 10px 10px rgba(0, 166, 188, 0.05),
    15px 25px 10px rgba(0, 166, 188, 0.1), 15px 20px 20px rgba(0, 166, 188, 0.1),
    inset -10px -10px 15px rgba(0, 166, 188, 0.5);
  border-radius: 50%;
}

.btns::before {
  content: "";
  position: absolute;
  top: 15px;
  left: 30px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #fff;
  opacity: 0.45;
}
</style>