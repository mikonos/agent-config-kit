# API / Backend Test Add-On

Use when the requirement is an API, backend service, job, queue, data sync, permission service, or integration.

## Coverage

- Request schema validation.
- Required/optional parameters.
- Boundary values.
- Authentication.
- Authorization.
- Idempotency.
- Duplicate request.
- Pagination.
- Sorting.
- Filtering.
- Rate limit.
- Timeout.
- Retry.
- Partial failure.
- Transaction rollback.
- Database consistency.
- Event ordering.
- Message queue delivery.
- Audit log.
- Backward compatibility.

## Useful TC Modules

```text
接口鉴权
参数校验
业务规则
状态流转
幂等与并发
数据一致性
异常与重试
日志与审计
兼容性
性能与限流
```

## Required Test Hooks

- Test account / token creation.
- Database query or fixture setup.
- Forced third-party timeout/error.
- Queue/job trigger.
- Log trace ID.
- Idempotency key control.
- Time simulation for expiry or scheduled jobs.

