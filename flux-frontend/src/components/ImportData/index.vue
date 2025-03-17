<template>
    <el-dialog
        v-model="visible"
        title="上传文件"
        width="500px"
        @close="handleClose"
    >
        <div>
            <el-upload
                v-if="showUpload"
                class="upload-box"
                :action="uploadImgUrl"
                :data="{ tableName }"
                :on-success="handleSuccess"
                :before-upload="beforeUpload"
                :headers="headers"
                accept=".xls,.xlsx"
                drag
            >
                <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                <div class="el-upload__text">拖拽或 <em>点击上传</em></div>
                <template #tip>
                    <div class="el-upload__tip">
                        仅支持 Excel 文件 (.xls, .xlsx)
                    </div>
                </template>
            </el-upload>

            <el-form v-else :model="targetForm" label-width="80px" ref="form">
                <el-form-item
                    v-for="column in tableColumns"
                    :key="column.name"
                    :label="
                        column.columnComment
                            ? column.columnComment
                            : column.columnName
                    "
                >
                    <el-select
                        v-model="targetForm[column.columnName]"
                        placeholder="请选择列绑定关系"
                    >
                        <el-option
                            v-for="excelCol in excelColumns"
                            :key="excelCol"
                            :label="excelCol"
                            :value="excelCol"
                        />
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleSubmit">
                        确定
                    </el-button>
                    <el-button @click="handleClose">取消</el-button>
                </el-form-item>
            </el-form>
        </div>
    </el-dialog>
</template>
  
  <script setup>
import { ref, defineProps, defineEmits } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import { ElLoading, ElMessage } from 'element-plus'
import { getToken } from '@/utils/auth'
import { tr } from 'element-plus/es/locales.mjs'

const excelColumns = ref([]) // Excel 表头
const tableColumns = ref([]) // 表格列

const targetForm = ref({}) // 表单数据

const uploadImgUrl = ref(
    import.meta.env.VITE_APP_BASE_API + '/import/uploadExcel'
) // 上传的图片服务器地址
const headers = ref({ Authorization: 'Bearer ' + getToken() })
const props = defineProps({
    tableName: {
        type: String,
        required: true // 确保 tableName 必传
    }
})

const emit = defineEmits(['update:modelValue', 'success'])

const visible = ref(true)
const showUpload = ref(true)

const handleClose = () => {
    emit('update:modelValue', false) // 关闭 dialog
}

const beforeUpload = (file) => {
    const isExcel =
        file.type === 'application/vnd.ms-excel' ||
        file.type ===
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    if (!isExcel) {
        ElMessage.error('只能上传 Excel 文件！')
        return false
    }
    return true
}

function handleSubmit() {
    console.log(targetForm.value)
}

const handleSuccess = (response) => {
    let result = response
    if (result.code === 200) {
        excelColumns.value = result.data.excelColumns
        tableColumns.value = result.data.tableColumns

        tableColumns.value.forEach((column) => {
            targetForm.value[column.columnName] = '' // 默认无选择
        })
        showUpload.value = false
    } else {
        ElMessage.error(result.msg)
    }
}
</script>
  
  <style scoped>
.upload-box {
    width: 100%;
    text-align: center;
}
</style>
  