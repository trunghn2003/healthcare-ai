package ai_service.model;

public @Bean
public RouterFunction<ServerResponse> orderDetailsRoute() {
    return RouterFunctions.route(
        RequestPredicates.GET("/order-details/{orderId}"),
        request -> {
            String orderId = request.pathVariable("orderId");
            // Lấy thông tin đơn hàng
            Mono<OrderInfo> orderInfo = webClient
                .get()
                .uri("http://order-service/orders/" + orderId)
                .retrieve()
                .bodyToMono(OrderInfo.class);
            // Lấy thông tin khách hàng
            Mono<CustomerInfo> customerInfo = webClient
                .get()
                .uri("http://customer-service/customers/{customerId}")
                .retrieve()
                .bodyToMono(CustomerInfo.class);
            // Kết hợp kết quả
            return Mono.zip(orderInfo, customerInfo)
                .flatMap(tuple -> {
                    OrderDetails combined = new OrderDetails();
                    combined.setOrderInfo(tuple.getT1());
                    combined.setCustomerInfo(tuple.getT2());
                    return ServerResponse.ok().bodyValue(combined);
                });
        }
    );
}
 {

}
