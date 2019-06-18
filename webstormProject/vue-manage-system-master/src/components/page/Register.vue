<template>
    <div class="login-wrap">
        <div class="ms-login">
            <div class="ms-title">后台管理系统</div>
            <el-card class="box-card box-card-left" style="padding: 30px 30px;" shadow="hover">
                <!--User信息-->
                <div class="form-box align-center" style="margin: 0 auto ;width: 60%">
                    <el-form ref="form" :model="form" label-width="80px">
                        <el-form-item label="姓名">
                            <el-input v-model="form.name"></el-input>
                        </el-form-item>

                        <el-form-item label="性别">
                            <el-radio-group v-model="form.resource">
                                <el-radio label="male">男</el-radio>
                                <el-radio label="female">女</el-radio>
                            </el-radio-group>
                        </el-form-item>
                        <el-form-item label="出身日期">
                            <el-col :span="11">
                                <el-date-picker type="date" placeholder="选择日期" v-model="form.date1" style="width: 100%;"></el-date-picker>
                            </el-col>
                        </el-form-item>

                        <el-form-item label="手机号">
                            <el-input v-model="form.name"></el-input>
                        </el-form-item>

                        <el-form-item label="验证码" style="display: inline-block">
                            <el-input v-model="form.desc" style="width: 40%"></el-input>
                            &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
                            <el-button type="primary" @click="sendVerifyCode">发送验证码</el-button>
                        </el-form-item>

                        <el-form-item label="邮箱">
                            <el-input v-model="form.name"></el-input>
                        </el-form-item>

                        <div class="login-btn">
                            <el-button type="primary" style="width: 85%;float: right" @click="submitForm('ruleForm')">注册</el-button>
                        </div>
                    </el-form>
                </div>
            </el-card>

        </div>
    </div>
</template>

<script>
    export default {
        data: function(){
            return {
                ruleForm: {
                    username: 'admin',
                    password: '123123'
                },
                rules: {
                    username: [
                        { required: true, message: '请输入用户名', trigger: 'blur' }
                    ],
                    password: [
                        { required: true, message: '请输入密码', trigger: 'blur' }
                    ]
                },
                form: {
                    name: '',
                    region: '',
                    date1: '',
                    date2: '',
                    delivery: true,
                    type: ['步步高'],
                    resource: '小天才',
                    desc: '',
                    options: []
                },
            }
        },
        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        localStorage.setItem('ms_username',this.ruleForm.username);
                        this.$router.push('/');
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            sendVerifyCode(){

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
        color: rgba(0, 0, 0, 1);
        border-bottom: 1px solid #ddd;
    }
    .ms-login{
        position: absolute;
        left:40%;
        top:30%;
        width:800px;
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
        font-size:12px;
        line-height:30px;
        color:#fff;
    }
</style>
