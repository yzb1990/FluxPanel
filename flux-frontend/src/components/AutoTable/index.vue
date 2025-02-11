<!-- tablePlus:二次封装table -->
<template>
    <el-table
        header-cell-class-name="tableHeader"
        stripe
        v-loading="loading"
        :data="tableData"
        :max-height="tableHeight"
        :border="stripe"
        @header-dragend="headerDragend"
        highlight-current-row
        ref="multipleTable"
        class="mytable"
    >
        <template v-for="(item, index) in columns">
            <el-table-column
                v-if="item.show == 1"
                :key="index"
                :prop="item.prop"
                :align="item.align"
                :label="item.label"
                :sortable="item.sortable != 0"
                :width="item.width"
                :fixed="item.fixed != 0"
                :show-overflow-tooltip="item.tooltip != 0"
            >
                <template #default="scope" v-if="$slots[item.prop]">
                    <slot :name="item.prop" v-bind="scope"></slot>
                </template>
            </el-table-column>
        </template>
    </el-table>
</template>

<script>
export default {
    name: 'CustomTable',
    props: {
        tableData: {
            type: Array,
            required: true
        },
        columns: {
            type: Array,
            required: true
        },
        loading: {
            type: Boolean,
            default: false
        },
        stripe: {
            type: Boolean,
            default: true
        }
    }
}
</script>

<style lang='scss' scoped>
.mytable {
    margin-top: 10px;
}

.disabled_class {
    color: #fff;
    background-color: #fab6b6;
    border-color: #fab6b6;
}

.disabled_class:hover {
    cursor: not-allowed;
}
</style>