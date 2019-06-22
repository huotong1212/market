<template>
    <div class="login-wrap">
        <div class="ms-login">
            <div class="ms-title">后台管理系统</div>
            <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="0px" class="ms-content">
                <p class="login-tips">请输入您的邮箱，我们将向其发送验证码</p>
                <el-form-item prop="email" >
                    <el-input v-model="ruleForm.email" placeholder="email" >
                        <el-button slot="prepend" icon="el-icon-eleme"></el-button>
                    </el-input>

                </el-form-item>
                <el-form-item prop="code" style="display: inline-block;">
                    <el-input style="width: 38%" v-model="ruleForm.code" @keyup.enter.native="submitForm('ruleForm')">
                        <el-button slot="prepend" icon="el-icon-lx-lock"></el-button>
                    </el-input>
                    &emsp;&emsp;&emsp;&emsp;&emsp;
                    <el-button type="primary" @click="sendVerifyCode()">{{text}}</el-button>
                </el-form-item>
                <span v-show="errorMessage" style="font-size: small;color: #f02d2d">邮箱不正确，不存在该用户</span>
                <span style="font-size: small;color: #f02d2d">{{checkError}}</span>
                <div class="login-btn">
                    <el-button type="primary" @click="checkEmailCode('ruleForm')">确定</el-button>
                </div>
<!--                <p class="login-tips">Tips : 用户名和密码随便填。</p>-->
            </el-form>
        </div>
    </div>
</template>

<script>
    import customValidate from "../utils/customValidate";
    import {checkEmailCode, getEmailCode} from "../api/api";

    export default {
        data: function(){
            return {
                ruleForm: {
                    email: '',
                    code: ''
                },
                rules: {
                    code: [
                        { required: true, message: '请输入验证码', trigger: 'blur' },
                        { min: 4, max: 4, message: '长度为 4 个字符'}
                    ],
                    email: [
                        { required: true, message: '请输入邮箱地址', trigger: 'blur' },
                        { validator: customValidate.isEmail, trigger: 'blur' }
                    ],
                },
                text:'获取验证码',
                flag:false,
                countdown : 60,
                errorMessage:false,
                checkError:''
            }
        },
        methods: {
            submitForm(formName) {
                // this.$refs[formName].validate((valid) => {
                //     if (valid) {
                //         localStorage.setItem('ms_username',this.ruleForm.username);
                //         this.$router.push('/');
                //     } else {
                //         console.log('error submit!!');
                //         return false;
                //     }
                // });
            },

            sendVerifyCode(){
                this.errorMessage = false
                this.$refs.ruleForm.validateField('email',(errorMessage => {
                    console.log('error',errorMessage)
                    if(errorMessage){
                        return
                    }
                    this.setTime()
                    getEmailCode({
                        email:this.ruleForm.email
                    }).then((response)=>{
                        console.log('EMailCode',response)
                    }).catch((error)=>{
                        console.log('EMailCodeError',error)
                        if(error.email[0].includes("邮箱不正确，不存在该用户")){
                            this.errorMessage = true
                        }
                    })

                }))
            },
            setTime() {
                if (this.countdown === 0) {
                    this.flag = false
                    this.text="获取验证码";
                    this.countdown = 60;
                } else {
                    this.flag = true
                    this.text="重新发送(" + this.countdown + ")";
                    this.countdown--;
                    setTimeout(()=>{
                        this.setTime()
                    },1000)
                }
            },
            checkEmailCode(formName){
                this.checkError = ''
                this.$refs[formName].validate((valid) => {
                    if(valid){
                        checkEmailCode(
                            this.ruleForm
                        ).then((response)=>{
                            console.log('checkEmailCode',response)
                            //存储在store
                            const loginInfo = {
                                username: response.data.name,
                                token: response.data.token
                            }
                            // 更新store数据
                            this.$store.dispatch('setInfo', loginInfo);
                            //跳转到首页页面
                            this.$router.push('../setPassword');
                        }).catch((error)=>{
                            console.log('error',error)
                            this.checkError = error.code[0]
                        })
                    }
                });

            }
        }
    }
</script>

<style scoped>
    .login-wrap{
        position: relative;
        width:100%;
        height:100%;
        background-image: url(../../assets/img/login-bg.jpg);
        background-size: 100%;
    }
    .ms-title{
        width:100%;
        line-height: 50px;
        text-align: center;
        font-size:20px;
        color: #fff;
        border-bottom: 1px solid #ddd;
    }
    .ms-login{
        position: absolute;
        left:50%;
        top:50%;
        width:350px;
        margin:-190px 0 0 -175px;
        border-radius: 5px;
        background: rgba(255,255,255, 0.3);
        overflow: hidden;
    }
    .ms-content{
        padding: 30px 30px;
    }
    .login-btn{
        text-align: center;
    }
    .login-btn button{
        width:100%;
        height:36px;
        margin-bottom: 10px;
    }
    .login-tips{
        font-size:18px;
        line-height:30px;
        color:#000000;
    }
</style>
