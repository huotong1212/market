<template>
    <div class="">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-copy"></i> tab选项卡</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-tabs v-model="message">
                <el-tab-pane :label="`我的信息`" name="first" style="display: inline-block">
                    <!--User信息-->
                    <div class="form-box align-center">
                        <el-form ref="form" status-icon :model="form" :rules="userRules" label-width="80px">
                            <el-form-item label="头像">
                                <div style="width: 50%">
                                    <div class="crop-demo" style="display: inline-block">
                                        <img :src="cropImg" class="pre-img">
                                        <div class="crop-demo-btn" style="display: inline-block">选择图片
                                            <input class="crop-input" type="file" name="image" accept="image/*"
                                                   @change="setImage"/>
                                        </div>
                                    </div>

                                    <el-dialog title="裁剪图片" :visible.sync="dialogVisible" width="30%">
                                        <vue-cropper ref='cropper' :src="imgSrc" :ready="cropImage" :zoom="cropImage"
                                                     :cropmove="cropImage"
                                                     style="width:100%;height:300px;"></vue-cropper>
                                        <span slot="footer" class="dialog-footer">
                                            <el-button @click="cancelCrop">取 消</el-button>
                                            <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
                                        </span>
                                    </el-dialog>
                                </div>
                            </el-form-item>

                            <el-form-item label="姓名">
                                <el-input v-model="form.username"></el-input>
                            </el-form-item>

                            <el-form-item label="性别">
                                <el-radio-group v-model="form.gender">
                                    <el-radio label="male">男</el-radio>
                                    <el-radio label="female">女</el-radio>
                                </el-radio-group>
                            </el-form-item>
                            <el-form-item label="出身日期">
                                <el-col :span="11">
                                    <el-date-picker type="date" placeholder="选择日期" value-format="yyyy-MM-dd"
                                                    v-model="form.birthday" style="width: 100%;"></el-date-picker>
                                </el-col>
                            </el-form-item>

                            <el-form-item label="邮箱">
                                <el-input :disabled="true" v-model="form.email"></el-input>
                            </el-form-item>

                            <el-form-item label="手机号">
                                <el-input :disabled="true" v-model="form.mobile"></el-input>
                            </el-form-item>

                            <div class="login-btn">
                                <el-button type="primary" style="width: 30%;float: right" @click="submitForm('form')">
                                    确定
                                </el-button>
<!--                                <el-button type="primary" style="width: 30%;float: right" @click="test">-->
<!--                                    测试-->
<!--                                </el-button>-->
                            </div>
                        </el-form>
                    </div>

                    <el-dialog
                            title="提示"
                            :visible.sync="MessageVisible"
                            width="30%"
                            :before-close="handleClose">
                        <span>{{hint}}</span>
                        <span slot="footer" class="dialog-footer">
<!--                            <el-button @click="dialogVisible = false">取 消</el-button>-->
                            <el-button type="primary" @click="MessageVisible = false">确 定</el-button>
                        </span>
                    </el-dialog>

                </el-tab-pane>
                <el-tab-pane :label="`已读消息(${read.length})`" name="second">
                    <template v-if="message === 'second'">
                        <el-table :data="read" :show-header="false" style="width: 100%">
                            <el-table-column>
                                <template slot-scope="scope">
                                    <span class="message-title">{{scope.row.title}}</span>
                                </template>
                            </el-table-column>
                            <el-table-column prop="date" width="150"></el-table-column>
                            <el-table-column width="120">
                                <template slot-scope="scope">
                                    <el-button type="danger" @click="handleDel(scope.$index)">删除</el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                        <div class="handle-row">
                            <el-button type="danger">删除全部</el-button>
                        </div>
                    </template>
                </el-tab-pane>
                <el-tab-pane :label="`回收站(${recycle.length})`" name="third">
                    <template v-if="message === 'third'">
                        <el-table :data="recycle" :show-header="false" style="width: 100%">
                            <el-table-column>
                                <template slot-scope="scope">
                                    <span class="message-title">{{scope.row.title}}</span>
                                </template>
                            </el-table-column>
                            <el-table-column prop="date" width="150"></el-table-column>
                            <el-table-column width="120">
                                <template slot-scope="scope">
                                    <el-button @click="handleRestore(scope.$index)">还原</el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                        <div class="handle-row">
                            <el-button type="danger">清空回收站</el-button>
                        </div>
                    </template>
                </el-tab-pane>
            </el-tabs>
        </div>
    </div>
</template>

<script>
    import VueCropper from 'vue-cropperjs';
    import {getUser, updateUserInfo} from "../api/api";
    import customValidate from "../utils/customValidate";
    import cookie from "../static/cookie";

    export default {
        name: 'userProfile',
        data() {
            return {
                file:'',
                hint:'',
                MessageVisible: false,
                message: 'first',
                showHeader: false,
                unread: [{
                    date: '2018-04-19 20:00:00',
                    title: '【系统通知】该系统将于今晚凌晨2点到5点进行升级维护',
                }, {
                    date: '2018-04-19 21:00:00',
                    title: '今晚12点整发大红包，先到先得',
                }],
                read: [{
                    date: '2018-04-19 20:00:00',
                    title: '【系统通知】该系统将于今晚凌晨2点到5点进行升级维护'
                }],
                recycle: [{
                    date: '2018-04-19 20:00:00',
                    title: '【系统通知】该系统将于今晚凌晨2点到5点进行升级维护'
                }],
                // defaultSrc: require('../../assets/img/img.jpg'),
                defaultSrc: '',
                fileList: [],
                imgSrc: '',
                cropImg: '',
                dialogVisible: false,
                rules: {
                    name: [
                        {required: true, message: '请输入活动名称', trigger: 'blur'},
                        {min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur'}
                    ],
                    region: [
                        {required: true, message: '请选择活动区域', trigger: 'change'}
                    ],
                    date1: [
                        {type: 'date', required: true, message: '请选择日期', trigger: 'change'}
                    ],
                    type: [
                        {type: 'array', required: true, message: '请至少选择一个活动性质', trigger: 'change'}
                    ],
                    resource: [
                        {required: true, message: '请选择活动资源', trigger: 'change'}
                    ],
                    desc: [
                        {required: true, message: '请填写活动形式', trigger: 'blur'}
                    ]
                },
                form: {
                    username: '',
                    password: '',
                    mobile: '',
                    email: '',
                    gender: '',
                    birthday: '',
                    portrait: '',
                },
                userRules: {
                    username: [
                        {required: true, message: '请输入用户名', trigger: 'blur'},
                        {min: 2, max: 8, message: '长度在 2 到 8 个字符'}
                    ],
                    password: [
                        {required: true, message: '请输入密码', trigger: 'blur'},
                        {min: 6, max: 20, message: '长度在 2 到 20 个字符'}
                    ],
                    mobile: [
                        {required: true, message: '请输入手机号码', trigger: 'blur'},
                        {validator: customValidate.isMobile, trigger: 'blur'}
                    ],
                    email: [
                        {required: true, message: '请输入邮箱地址', trigger: 'blur'},
                        {validator: customValidate.isEmail, trigger: 'blur'}
                    ],
                    code: [
                        {required: true, message: '请输入验证码', trigger: 'blur'},
                        {min: 4, max: 4, message: '长度为 4 个字符'}
                    ],
                    gender: [
                        {required: true, message: '请输入验证码', trigger: 'blur'},
                    ],
                    birthday: [
                        {required: true, message: '请输入出生年月', trigger: 'blur'},
                    ],
                },
            }
        },
        components: {
            VueCropper
        },
        methods: {
            handleRead(index) {
                const item = this.unread.splice(index, 1);
                console.log(item);
                this.read = item.concat(this.read);
            },
            handleDel(index) {
                const item = this.read.splice(index, 1);
                this.recycle = item.concat(this.recycle);
            },
            handleRestore(index) {
                const item = this.recycle.splice(index, 1);
                this.read = item.concat(this.read);
            },
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        //调用
                        let portrait = this.imgSrc?this.imgSrc:this.cropImg
                        let file = this.dataURLtoFile(portrait, this.file.name);

                        console.log('formData', this.form)
                        const formData = new FormData();
                        // 等同于使用map.entries()
                        for (let key in this.form) {
                            formData.append(key,this.form[key])
                        }
                        formData.set('portrait',this.file);

                        updateUserInfo(
                            // this.form
                            formData
                        ).then((response) => {
                            this.getUserInfo()
                            this.hint = '保存成功'
                            this.MessageVisible = true
                            console.log(response)
                            cookie.setCookie('userImage',response.data.portrait)
                        }).catch(function (error) {
                            console.log(error);
                        });
                    } else {
                        this.hint = '发出未知错误，报错失败，请再次尝试'
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            test(){
                // 等同于使用map.entries()
                console.log(this.form)
                let arr = Array.from(this.form)
                this.form.username = '321321'
                for (let key in this.form) {
                    // console.log("Key: %s, Value: %s", key, value);
                    console.log(this.form[key])
                    // formData.append(key,value)
                }

            },
            getUserInfo(){
                getUser().then((response)=> {
                    console.log(response)
                    this.form = response.data
                    this.cropImg = this.form.portrait
                }).catch(function (error) {
                    console.log(error);
                });
            },
            handleClose(done) {
                this.$confirm('确认关闭？')
                    .then(_ => {
                        done();
                    })
                    .catch(_ => {});
            },
            setImage(e) {
                const file = e.target.files[0];
                this.file = file
                console.log('file',file)
                if (!file.type.includes('image/')) {
                    return;
                }
                const reader = new FileReader();
                reader.onload = (event) => {
                    this.dialogVisible = true;
                    this.imgSrc = event.target.result;
                    this.$refs.cropper && this.$refs.cropper.replace(event.target.result);
                };
                reader.readAsDataURL(file);
            },
            cropImage() {
                this.cropImg = this.$refs.cropper.getCroppedCanvas().toDataURL();
            },
            cancelCrop() {
                this.dialogVisible = false;
                this.cropImg = this.defaultSrc;
            },
            imageuploaded(res) {
                console.log(res)
            },
            handleError() {
                this.$notify.error({
                    title: '上传失败',
                    message: '图片上传接口上传失败，可更改为自己的服务器接口'
                });
            },
            //将base64转换为文件
            dataURLtoFile: function(dataurl, filename) {
                var arr = dataurl.split(','),
                    mime = arr[0].match(/:(.*?);/)[1],
                    bstr = atob(arr[1]),
                    n = bstr.length,
                    u8arr = new Uint8Array(n);
                while (n--) {
                    u8arr[n] = bstr.charCodeAt(n);
                }
                return new File([u8arr], filename, { type: mime });
            },
        },
        created() {
            this.cropImg = this.defaultSrc;
            this.getUserInfo()
        },
        activated(){
            this.getUserInfo()
        },
        computed: {
            unreadNum() {
                return this.unread.length;
            }
        },
        mounted() {

        }
    }

</script>

<style>
    .message-title {
        cursor: pointer;
    }

    .handle-row {
        margin-top: 30px;
    }

    .content-title {
        font-weight: 400;
        line-height: 50px;
        margin: 10px 0;
        font-size: 22px;
        color: #1f2f3d;
    }

    .pre-img {
        width: 100px;
        height: 100px;
        background: #f8f8f8;
        border: 1px solid #eee;
        border-radius: 5px;
    }

    .crop-demo {
        display: flex;
        align-items: flex-end;
    }

    .crop-demo-btn {
        position: relative;
        width: 100px;
        height: 40px;
        line-height: 40px;
        padding: 0 20px;
        margin-left: 30px;
        background-color: #409eff;
        color: #fff;
        font-size: 14px;
        border-radius: 4px;
        box-sizing: border-box;
    }

    .crop-input {
        position: absolute;
        width: 100px;
        height: 40px;
        left: 0;
        top: 0;
        opacity: 0;
        cursor: pointer;
    }
</style>

