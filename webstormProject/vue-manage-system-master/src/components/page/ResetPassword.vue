<template>
    <div class="login-wrap">
        <div class="ms-login">
            <div class="ms-title">后台管理系统</div>
            <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="0px" class="ms-content">
                <p class="login-tips">请输入您的新密码</p>
                <el-form-item prop="first" >
                    <el-input v-model="ruleForm.first" placeholder="password" >
                        <el-button slot="prepend" icon="el-icon-lx-lock"></el-button>
                    </el-input>
                </el-form-item>
                <span class="login-tips">请再次输入</span>
                <el-form-item prop="second">
                    <el-input  v-model="ruleForm.second" placeholder="password" >
                        <el-button slot="prepend" icon="el-icon-lx-lock"></el-button>
                    </el-input>
                </el-form-item>
                <span v-show="errorMessage" style="font-size: small;color: #f02d2d">邮箱不正确，不存在该用户</span>
                <div class="login-btn">
                    <el-button type="primary" @click="submitForm('ruleForm')">确定</el-button>
                </div>
<!--                <p class="login-tips">Tips : 用户名和密码随便填。</p>-->
            </el-form>
        </div>
    </div>
</template>

<script>
    import customValidate from "../utils/customValidate";
    import {getEmailCode, resetPassword} from "../api/api";
    import cookie from "../static/cookie";

    export default {
        data: function(){
            return {
                ruleForm: {
                    first: '',
                    second: ''
                },
                rules: {
                    first: [
                        { required: true, message: '请输入密码', trigger: 'blur' },
                        { min: 6, max: 20, message: '长度为 6-20 个字符'},
                        { validator: this.validatePass, trigger: 'blur' }
                    ],
                    second: [
                        { required: true, message: '请再次输入', trigger: 'blur' },
                        { validator: this.validatePass2, trigger: 'blur' }
                    ],
                },
                errorMessage:false
            }
        },
        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        resetPassword({
                            password:this.ruleForm.first
                        }).then((response)=>{
                            console.log('success')
                            this.$message.success('密码修改成功');
                            setTimeout(()=>{
                                this.$router.push('/');
                            },1000)
                        }).catch(function (error) {

                        })
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },

            validatePass(rule, value, callback){
                if (value === '') {
                    callback(new Error('请输入密码'));
                } else {
                    if (this.ruleForm.second !== '') {
                        this.$refs.ruleForm.validateField('second');
                    }
                    callback();
                }
            },
            validatePass2(rule, value, callback){
                if (value === '') {
                    callback(new Error('请再次输入密码'));
                } else if (value !== this.ruleForm.first) {
                    callback(new Error('两次输入密码不一致!'));
                } else {
                    callback();
                }
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
