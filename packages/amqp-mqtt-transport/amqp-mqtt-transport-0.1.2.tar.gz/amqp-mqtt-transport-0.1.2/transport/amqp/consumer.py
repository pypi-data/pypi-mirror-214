from . import AMQPController, BindingsParams, QueueParams, ExchangeParams, setup_queue
import typing
import logging
import aio_pika
import transport.abc

__all__ = ['AMQPConsumer']
logger = logging.getLogger(__name__)


class AMQPConsumer(transport.abc.Consumer):
    def __init__(self, channel: aio_pika.abc.AbstractChannel):
        self._channel = channel

    @property
    def queue_name(self) -> str:
        return self._binding_params.queue_params.name

    @property
    def queue_params(self) -> QueueParams:
        return self._binding_params.queue_params

    @property
    def exchange_params(self) -> ExchangeParams:
        return self._binding_params.exchange_params

    @property
    def routing_key(self) -> str:
        return self._binding_params.routing_key

    def set_up_binding_params(self, binding_params: BindingsParams):
        self._binding_params = binding_params

    async def create_queue(self):
        if self._binding_params is None:
            raise ValueError(
                'Configuration needed to setup queue is not exist, call set_up_binding_params(BindingsParams) with queue configuration')
        # Binding queue and exchange
        self._exchange, self._queue = await setup_queue(self._binding_params, self._channel)

    async def replace_channel(self, channel: aio_pika.abc.AbstractChannel):
        await self._channel.close()
        self._channel = channel
        self._queue.channel = self._channel.channel
        # await self.create_queue()
        # await self.subscribe(self._message_handler)

    async def subscribe(self, message_handler: typing.Callable):
        self._message_handler = message_handler
        await self._queue.consume(self._message_handler)
