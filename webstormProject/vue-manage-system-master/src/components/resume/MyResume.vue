<template>
    <div class="table">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-cascades"></i> 我的简历</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="handle-box">
                <el-button type="primary" icon="delete" class="handle-del mr10" @click="delAll">批量删除</el-button>
                <el-select v-model="select_cate" placeholder="筛选语言" class="handle-select mr10">
                    <el-option v-for="index in classification" :key="Number(index)" :label="languageList[index]"
                               :value="Number(index)"></el-option>
                </el-select>
                <el-input v-model="select_word" placeholder="筛选关键词" class="handle-input mr10"></el-input>
                <el-button type="primary" icon="search" @click="search">搜索</el-button>
                <el-button type="primary" icon="el-icon-circle-plus-outline" class="handle-create"
                           @click="createResume">创建简历
                </el-button>
            </div>
            <el-table :data="tableData" border class="table" ref="multipleTable"
                      @selection-change="handleSelectionChange" @sort-change="handleSortChange">
                <el-table-column type="selection" width="55" align="center"></el-table-column>
                <el-table-column prop="add_time" label="创建日期" :formatter="dateFormat" sortable width="150">
                </el-table-column>
                <el-table-column prop="language" label="语言" :formatter="languageFormat" sortable width="120">
                </el-table-column>
                <el-table-column prop="name" label="简历名称">
                    <template slot-scope="scope">
                        <el-link @click="showResume(scope.$index, scope.row)" :underline="false">{{scope.row.name}}<i class="el-icon-view el-icon--right"/></el-link>
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="180" align="center">
                    <template slot-scope="scope">
                        <el-button type="text" icon="el-icon-edit" @click="handleEdit(scope.$index, scope.row)">编辑
                        </el-button>
                        <el-button type="text" icon="el-icon-tickets" @click="Navigate(scope.$index, scope.row)">查看
                        </el-button>
                        <el-button type="text" icon="el-icon-delete" class="red"
                                   @click="handleDelete(scope.$index, scope.row)">删除
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
            <div class="pagination">
                <el-pagination background @current-change="handleCurrentChange" layout="prev, pager, next"
                               :page-count="6" :total="total_page">
                </el-pagination>
            </div>
        </div>

        <!-- 编辑弹出框 -->
        <el-dialog title="编辑" :visible.sync="editVisible" width="30%">
            <el-form ref="form" :model="form" label-width="50px">
                <el-form-item label="日期">
                    <el-date-picker type="date" placeholder="选择日期" v-model="form.date" value-format="yyyy-MM-dd"
                                    style="width: 100%;"></el-date-picker>
                </el-form-item>
                <el-form-item label="姓名">
                    <el-input v-model="form.name"></el-input>
                </el-form-item>
                <el-form-item label="地址">
                    <el-input v-model="form.address"></el-input>
                </el-form-item>

            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>

        <!-- 删除提示框 -->
        <el-dialog title="提示" :visible.sync="delVisible" width="300px" center>
            <div class="del-dialog-cnt">删除不可恢复，是否确定删除？</div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="delVisible = false">取 消</el-button>
                <el-button type="primary" @click="deleteRow">确 定</el-button>
            </span>
        </el-dialog>

        <!-- 编辑/创建简历弹出框 -->
        <el-dialog :title="createOrUpdate?'创建简历':'编辑简历'" :visible.sync="createVisible" width="30%">
            <el-form ref="Resume" :rules="ResumeRules" :model="Resume" status-icon label-width="80px">
                <el-form-item label="简历名称" prop="name">
                    <el-input v-model="Resume.name" placeholder="请输入简历名称"></el-input>
                </el-form-item>
                <el-form-item label="语言">
                    <el-select v-model="Resume.language" placeholder="请选择语言类型" prop="language">
                        <el-option v-for="index in classification" :key="Number(index)" :label="languageList[index]"
                                   :value="Number(index)"></el-option>
                    </el-select>
                </el-form-item>

            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="createVisible = false">取 消</el-button>
                <el-button type="primary" @click="crOrUpUserResume('Resume')">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    import customValidate from "../utils/customValidate";
    import {
        createResumeCode,
        createUserResume,
        deleteUserResume,
        getAllUserResume,
        getUserResume,
        updateUserResume
    } from "../api/api";
    import cookie from "../static/cookie";
    import Vue from "vue";

    export default {
        name: 'MyResume',
        data() {
            return {
                url: './vuetable.json',
                tableData: [],
                cur_page: 1,
                multipleSelection: [],
                select_cate: '',
                select_word: '',
                del_list: [],
                is_search: false,
                editVisible: false,
                delVisible: false,
                createVisible: false,
                form: {
                    name: '',
                    date: '',
                    address: ''
                },
                idx: -1,
                id: -1,
                Resume: {
                    id: '',
                    name: '',
                    language: '',
                },
                ResumeRules: {
                    name: [
                        {required: true, message: '请输入简历名称', trigger: 'blur'},
                        {max: 30, message: '长度超出范围'}
                    ],
                    language: [
                        {required: true, message: '请选择语言', trigger: 'blur'},
                    ],
                },
                count: 0,
                page_size: 8,
                languageList: {
                    0: '中文',
                    1: '英语',
                    2: '日语'
                },
                createOrUpdate: false, // true-->create  false-->update
                params: {
                    page: 1,
                    ordering: '',
                    language:'',
                    search:'',
                }
            }
        },
        created() {
            this.getData();
        },
        watch:{
            select_cate(val){
                this.params.language = val
                this.getData()
            }
        },
        computed: {
            // data() {
            //     return this.tableData.filter((d) => {
            //         let is_del = false;
            //         for (let i = 0; i < this.del_list.length; i++) {
            //             if (d.name === this.del_list[i].name) {
            //                 is_del = true;
            //                 break;
            //             }
            //         }
            //         if (!is_del) {
            //             if (d.address.indexOf(this.select_cate) > -1 &&
            //                 (d.name.indexOf(this.select_word) > -1 ||
            //                     d.address.indexOf(this.select_word) > -1)
            //             ) {
            //                 return d;
            //             }
            //         }
            //     })
            // },
            total_page() {
                let num = Math.ceil(this.count / this.page_size)
                return num * 10
            },
            selectedId() {
                const selectedId = []
                this.multipleSelection.forEach((item) => {
                    selectedId.push(item.id)
                })
                return selectedId
            },
            classification() {
                return Object.keys(this.languageList)
            }
        },
        methods: {
            showResume(index, row){
                createResumeCode({
                    resumeId:row.id
                }).then((response)=>{
                    console.log(response)
                    let code = response.data.code
                    let routeUrl = this.$router.resolve({
                        path: "../showResume",
                        query: {code:code}
                    });
                    window.open(routeUrl .href, '_blank');
                }).catch(function (error) {

                })
            },

            createResume() {
                this.Resume = {
                    name: '',
                    language: '',
                }
                this.createVisible = true;
                this.createOrUpdate = true
            },
            // 分页导航
            handleCurrentChange(val) {
                this.cur_page = val;
                this.params.page = val
                this.getData();
            },
            handleSortChange(payload) {
                console.log('handleSortChange', payload)
                switch (payload.prop) {
                    case 'add_time':
                        if(payload.prop==='ascending'){
                            this.params.ordering = 'add_time';
                        }else if(payload.prop==='descending'){
                            this.params.ordering = '-add_time';
                        }
                        this.getData()
                        break;
                    case 'language':
                        if(payload.prop==='ascending'){
                            this.params.ordering = 'language';
                        }else if(payload.prop==='descending'){
                            this.params.ordering = '-language';
                        }
                        this.getData()
                        break;
                }
            },
            // 获取 easy-mock 的模拟数据
            getData() {
                // 开发环境使用 easy-mock 数据，正式环境使用 json 文件
                // if (process.env.NODE_ENV === 'development') {
                //     this.url = '/ms/table/list';
                // };
                // this.$axios.post(this.url, {
                //     page: this.cur_page
                // }).then((res) => {
                //     this.tableData = res.data.list;
                // })

                getAllUserResume(this.params).then((response) => {
                    console.log('getAllUserResume', response.data)
                    this.tableData = response.data.results
                    this.count = response.data.count
                }).catch(function (error) {
                    console.log('error', error)
                })
            },
            dateFormat(row, column) {
                return new Date(row.add_time).toLocaleDateString()
            },
            languageFormat(row, column) {
                return this.languageList[row.language]
            },
            search() {
                this.params.search = this.select_word
                this.getData()
                this.is_search = true;
            },
            formatter(row, column) {
                return row.address;
            },
            filterTag(value, row) {
                return row.tag === value;
            },
            handleEdit(index, row) {
                console.log(index, row)
                this.idx = index;
                this.id = row.id;
                this.Resume = {
                    id: row.id,
                    name: row.name,
                    language: row.language,
                }
                this.createVisible = true;
                this.createOrUpdate = false;
            },
            Navigate(index, row) {
                //本地存储用户信息
                cookie.setCookie('resumeId', row.id, 7);

                //存储在store
                // 更新store数据
                this.$store.dispatch('setResumeId', row.id);
                //跳转到创建页面
                this.createVisible = false;
                this.$router.push({path: '../resume', params: {}})
            },

            handleDelete(index, row) {
                this.delVisible = true;
                this.idx = index;
                this.id = row.id;
            },
            delAll() {
                console.log(this.selectedId)
                deleteUserResume(
                    1,
                    {
                        type: 'deleteAll',
                        selectedId: this.selectedId
                    }
                ).then((response) => {
                    console.log('handleDelete', response)
                    this.clearTable()
                    this.getData()
                    // this.tableData.splice(index,1) //['a','c','d'] 删除起始下标为1，长度为1的一个值，len设置的1，如果为0，则数组不变
                }).catch(function () {

                })
                // const length = this.multipleSelection.length;
                // let str = '';
                // this.del_list = this.del_list.concat(this.multipleSelection);
                // for (let i = 0; i < length; i++) {
                //     str += this.multipleSelection[i].name + ' ';
                // }
                // this.$message.error('删除了' + str);
                // this.multipleSelection = [];
            },
            handleSelectionChange(val) {
                this.multipleSelection = val;
            },
            clearTable() {
                this.selectedId.forEach((id) => {
                    let index = this.tableData.findIndex(item => item.id === id);
                    this.tableData.splice(index, 1) //['a','c','d'] 删除起始下标为1，长度为1的一个值，len设置的1，如果为0，则数组不变
                })
                this.multipleSelection = []
            },

            // 保存编辑
            saveEdit() {
                // this.editVisible = false;
                // this.$message.success(`修改第 ${this.idx+1} 行成功`);
                // if(this.tableData[this.idx].id === this.id){
                //     this.$set(this.tableData, this.idx, this.form);
                // }else{
                //     for(let i = 0; i < this.tableData.length; i++){
                //         if(this.tableData[i].id === this.id){
                //             this.$set(this.tableData, i, this.form);
                //             return ;
                //         }
                //     }
                // }
            },

            crOrUpUserResume(formName) {
                console.log(this.createOrUpdate)
                if (this.createOrUpdate) {
                    console.log('------create')
                    this.createUserResume(formName)
                } else {
                    console.log('------update')
                    this.updateUserResume(formName)
                }
            },

            updateUserResume(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        let resume = this.tableData.find(item => item.id === this.Resume.id)
                        console.log('before', resume)
                        updateUserResume(
                            this.Resume.id,
                            this.Resume
                        ).then((response) => {
                            console.log(response)

                            Vue.set(resume, 'language', response.data.language)
                            Vue.set(resume, 'name', response.data.name)
                            console.log('after', resume)

                            this.createVisible = false
                        }).catch(function (error) {
                            console.log(error)
                        })
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },

            // 创建简历
            createUserResume(formName) {
                this.$refs[formName].validate((valid) => {
                    console.log('valid', valid)
                    if (valid) {
                        console.log('Resume', this.Resume)
                        // this.$refs[formName].resetFields();//将form表单重置
                        createUserResume(
                            this.Resume
                        ).then((response) => {
                            //console.log('createResume',response);
                            //本地存储用户信息
                            cookie.setCookie('resumeId', response.data.id, 7);

                            //存储在store
                            // 更新store数据
                            this.$store.dispatch('setResumeId', response.data.id);
                            //跳转到创建页面
                            // console.log(this.$router) //vuerouter对象
                            // console.log(this.$route) //创建的routes路由
                            this.createVisible = false;
                            this.$router.push({path: '../resume', params: {}})
                        }).catch(function (error) {
                            console.log(error);
                        });
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });


            },
            // 确定删除
            deleteRow() {
                deleteUserResume(
                    this.id,
                    {}
                ).then((response) => {
                    console.log('handleDelete', response)
                    this.tableData.splice(this.idx, 1) //['a','c','d'] 删除起始下标为1，长度为1的一个值，len设置的1，如果为0，则数组不变
                    this.$message.success('删除成功');
                    this.delVisible = false;
                }).catch(function () {

                })

                // this.$message.success('删除成功');
                // this.delVisible = false;
                // if(this.tableData[this.idx].id === this.id){
                //     this.tableData.splice(this.idx, 1);
                // }else{
                //     for(let i = 0; i < this.tableData.length; i++){
                //         if(this.tableData[i].id === this.id){
                //             this.tableData.splice(i, 1);
                //             return ;
                //         }
                //     }
                // }
            }
        }
    }

</script>

<style scoped>
    .handle-box {
        margin-bottom: 20px;
    }

    .handle-select {
        width: 120px;
    }

    .handle-create {
        float: right;
    }

    .handle-input {
        width: 300px;
        display: inline-block;
    }

    .del-dialog-cnt {
        font-size: 16px;
        text-align: center
    }

    .table {
        width: 100%;
        font-size: 14px;
    }

    .red {
        color: #ff0000;
    }

    .mr10 {
        margin-right: 10px;
    }
</style>
