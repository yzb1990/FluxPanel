<template>
    <div class="app-container">
        <el-form
            :model="queryParams"
            ref="multipleForm"
            :inline="true"
            v-show="showSearch"
            label-width="68px"
        >
            <el-form-item label="小车名称" prop="carName">
                <el-input
                    v-model="queryParams.carName"
                    placeholder="请输入小车名称"
                    clearable
                    @keyup.enter="handleQuery"
                />
            </el-form-item>

            <el-form-item label="车辆类型" prop="carType">
                <el-select
                    v-model="queryParams.carType"
                    placeholder="请选择车辆类型"
                    style="width: 180px"
                    clearable
                >
                    <el-option
                        v-for="dict in car_type"
                        :key="dict.value"
                        :label="dict.label"
                        :value="dict.value"
                    />
                </el-select>
            </el-form-item>

            <el-form-item label="创建时间" style="width: 308px">
                <el-date-picker
                    v-model="daterangeCreateTime"
                    value-format="YYYY-MM-DD"
                    type="daterange"
                    range-separator="-"
                    start-placeholder="开始日期"
                    end-placeholder="结束日期"
                ></el-date-picker>
            </el-form-item>

            <el-form-item label="经度" prop="lng">
                <el-input
                    v-model="queryParams.lng"
                    placeholder="请输入经度"
                    clearable
                    @keyup.enter="handleQuery"
                />
            </el-form-item>

            <el-form-item label="所在位置" prop="location">
                <el-input
                    v-model="queryParams.location"
                    placeholder="请输入所在位置"
                    clearable
                    @keyup.enter="handleQuery"
                />
            </el-form-item>
            <el-form-item>
                <el-button type="primary" icon="Search" @click="handleQuery"
                    >搜索</el-button
                >
                <el-button icon="Refresh" @click="resetQuery">重置</el-button>
            </el-form-item>
        </el-form>

        <el-card class="base-table" ref="fullTable">
            <TableSetup
                ref="tSetup"
                @onStripe="onStripe"
                @onRefresh="onRefresh"
                @onChange="onChange"
                @onfullTable="onfullTable"
                @onSearchChange="onSearchChange"
                :columns="columns"
                :isTable="isTable"
            >
                <template v-slot:operate>
                    <el-button
                        type="primary"
                        plain
                        icon="Plus"
                        @click="handleAdd"
                        v-hasPermi="['car:info:add']"
                        >新增</el-button
                    >
                    <el-button
                        type="success"
                        plain
                        icon="Edit"
                        :disabled="single"
                        @click="handleUpdate"
                        v-hasPermi="['car:info:edit']"
                        >修改</el-button
                    >
                    <el-button
                        type="danger"
                        plain
                        icon="Delete"
                        :disabled="multiple"
                        @click="handleDelete"
                        v-hasPermi="['car:info:remove']"
                        >删除</el-button
                    >
                    <el-button
                        type="warning"
                        plain
                        icon="Download"
                        @click="handleExport"
                        v-hasPermi="['car:info:export']"
                        >导出</el-button
                    >
                </template>
            </TableSetup>
            <auto-table
                ref="multipleTable"
                class="mytable"
                :tableData="infoList"
                :columns="columns"
                :loading="loading"
                :stripe="stripe"
                :tableHeight="tableHeight"
                @onColumnWidthChange="onColumnWidthChange"
                @onSelectionChange="handleSelectionChange"
            >
                <template #operate="{ row }">
                    <el-button
                        link
                        type="primary"
                        icon="Edit"
                        @click="handleUpdate(row)"
                        v-hasPermi="['partner:info:edit']"
                        >修改</el-button
                    >
                    <el-button
                        link
                        type="primary"
                        icon="Delete"
                        @click="handleDelete(row)"
                        v-hasPermi="['partner:info:remove']"
                        >删除</el-button
                    >
                </template>
            </auto-table>
            <div class="table-pagination">
                <pagination
                    v-show="total > 0"
                    :total="total"
                    v-model:page="queryParams.pageNum"
                    v-model:limit="queryParams.pageSize"
                    @pagination="getList"
                />
            </div>
        </el-card>

        <!-- 添加或修改小车信息对话框 -->
        <el-dialog :title="title" v-model="open" width="800px" append-to-body>
            <el-form
                ref="infoRef"
                :model="form"
                :rules="rules"
                label-width="80px"
            >
                <el-form-item label="小车名称" prop="carName">
                    <el-input
                        v-model="form.carName"
                        placeholder="请输入小车名称"
                    />
                </el-form-item>

                <el-form-item label="车辆类型" prop="carType">
                    <el-select
                        v-model="form.carType"
                        placeholder="请选择车辆类型"
                    >
                        <el-option
                            v-for="dict in car_type"
                            :key="dict.value"
                            :label="dict.label"
                            :value="parseInt(dict.value)"
                        ></el-option>
                    </el-select>
                </el-form-item>

                <el-form-item label="图片" prop="image">
                    <el-input v-model="form.image" placeholder="请输入图片" />
                </el-form-item>

                <el-form-item label="纬度" prop="lat">
                    <el-input v-model="form.lat" placeholder="请输入纬度" />
                </el-form-item>

                <el-form-item label="经度" prop="lng">
                    <el-input v-model="form.lng" placeholder="请输入经度" />
                </el-form-item>

                <el-form-item label="所在位置" prop="location">
                    <el-input
                        v-model="form.location"
                        placeholder="请输入所在位置"
                    />
                </el-form-item>

                <el-form-item label="管理员ID" prop="manager">
                    <el-input
                        v-model="form.manager"
                        placeholder="请输入管理员ID"
                    />
                </el-form-item>

                <el-form-item label="价格" prop="price">
                    <el-input v-model="form.price" placeholder="请输入价格" />
                </el-form-item>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button type="primary" @click="submitForm"
                        >确 定</el-button
                    >
                    <el-button @click="cancel">取 消</el-button>
                </div>
            </template>
        </el-dialog>
    </div>
</template>

<script setup name="Info">
import { listInfo, getInfo, delInfo, addInfo, updateInfo } from '@/api/car/info'
import { listAllTable } from '@/api/system/table'
import TableSetup from '@/components/TableSetup'
import AutoTable from '@/components/AutoTable'
import { onMounted } from 'vue'
const { proxy } = getCurrentInstance()
const { car_type } = proxy.useDict('car_type')

const infoList = ref([])
const open = ref(false)
const loading = ref(true)
const showSearch = ref(true)
const ids = ref([])
const single = ref(true)
const multiple = ref(true)
const total = ref(0)
const title = ref('')
const daterangeCreateTime = ref([])

const columns = ref([])
const stripe = ref(true)
const isTable = ref(true)
const tableHeight = ref(500)

const data = reactive({
    form: {},
    queryParams: {
        pageNum: 1,
        pageSize: 10,
        carName: null,
        carType: null,
        createTime: null,
        lng: null,
        location: null
    },
    rules: {
        carName: [
            { required: true, message: '小车名称不能为空', trigger: 'blur' }
        ],
        carType: [
            { required: true, message: '车辆类型不能为空', trigger: 'change' }
        ],
        location: [
            { required: true, message: '所在位置不能为空', trigger: 'blur' }
        ]
    }
})

const { queryParams, form, rules } = toRefs(data)

/** 查询小车信息列表 */
function getList() {
    loading.value = true
    queryParams.value.params = {}
    if (null != daterangeCreateTime && '' != daterangeCreateTime) {
        queryParams.value.params['beginCreateTime'] =
            daterangeCreateTime.value[0]
        queryParams.value.params['endCreateTime'] = daterangeCreateTime.value[1]
    }
    listInfo(queryParams.value).then((response) => {
        infoList.value = response.rows
        total.value = response.total
        loading.value = false
    })
}

function getColumns() {
    listAllTable({ tableName: 'car_info' })
        .then((response) => {
            columns.value = response.data
        })
        .then(() => {
            getList()
        })
}

// 取消按钮
function cancel() {
    open.value = false
    reset()
}

// 表单重置
function reset() {
    form.value = {
        carName: null,
        carType: null,
        createTime: null,
        delFlag: null,
        id: null,
        image: null,
        lat: null,
        lng: null,
        location: null,
        manager: null,
        price: null,
        updateTime: null
    }
    proxy.resetForm('infoRef')
}

/** 搜索按钮操作 */
function handleQuery() {
    queryParams.value.pageNum = 1
    getList()
}

/** 重置按钮操作 */
function resetQuery() {
    daterangeCreateTime.value = []
    proxy.resetForm('multipleForm')
    handleQuery()
}

// 多选框选中数据
function handleSelectionChange(selection) {
    ids.value = selection.map((item) => item.id)
    single.value = selection.length != 1
    multiple.value = !selection.length
}

/** 新增按钮操作 */
function handleAdd() {
    reset()
    open.value = true
    title.value = '添加小车信息'
}

/** 修改按钮操作 */
function handleUpdate(row) {
    reset()
    const carInfoId = row.id || ids.value
    getInfo(carInfoId).then((response) => {
        form.value = response.data
        open.value = true
        title.value = '修改小车信息'
    })
}

/** 提交按钮 */
function submitForm() {
    proxy.$refs['infoRef'].validate((valid) => {
        if (valid) {
            if (form.value.id != null) {
                updateInfo(form.value).then((response) => {
                    proxy.$modal.msgSuccess('修改成功')
                    open.value = false
                    getList()
                })
            } else {
                addInfo(form.value).then((response) => {
                    proxy.$modal.msgSuccess('新增成功')
                    open.value = false
                    getList()
                })
            }
        }
    })
}

/** 删除按钮操作 */
function handleDelete(row) {
    const _ids = row.id || ids.value
    proxy.$modal
        .confirm('是否确认删除小车信息编号为"' + _ids + '"的数据项？')
        .then(function () {
            return delInfo(_ids)
        })
        .then(() => {
            getList()
            proxy.$modal.msgSuccess('删除成功')
        })
        .catch(() => {})
}

/** 导出按钮操作 */
function handleExport() {
    proxy.download(
        'car/info/export',
        {
            ...queryParams.value
        },
        `info_${new Date().getTime()}.xlsx`
    )
}

//表格全屏
function onfullTable() {
    proxy.$refs.tSetup.onFull(proxy.$refs.fullTable.$el)
}
//表格刷新
function onRefresh() {
    getList()
}
//搜索框显示隐藏
function onSearchChange() {
    showSearch.value = !showSearch.value
}

function onStripe(val) {
    stripe.value = val
}
//改变表头数据
function onChange(val) {
    columns.value = val
}

//改变表格宽度
function onColumnWidthChange(column) {
    proxy.$refs.tSetup.tableWidth(column)
}

getColumns()
</script>
