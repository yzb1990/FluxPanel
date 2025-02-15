import request from '@/utils/request'

// 查询汽车销售列表
export function listSeller(query) {
  return request({
    url: '/car/seller/list',
    method: 'get',
    params: query
  })
}

// 查询汽车销售详细
export function getSeller(id) {
  return request({
    url: '/car/seller/getById/' + id,
    method: 'get'
  })
}

// 新增汽车销售
export function addSeller(data) {
  return request({
    url: '/car/seller/add',
    method: 'post',
    data: data
  })
}

// 修改汽车销售
export function updateSeller(data) {
  return request({
    url: '/car/seller/update',
    method: 'put',
    data: data
  })
}

// 删除汽车销售
export function delSeller(id) {
  return request({
    url: '/car/seller/delete/' + id,
    method: 'delete'
  })
}