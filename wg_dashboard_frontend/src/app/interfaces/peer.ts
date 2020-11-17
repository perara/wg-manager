export interface Peer {
  _stats: any;
  address: string;
  v6_address: string;
  public_key: string;
  private_key: string;
  shared_key: string;
  dns: string;
  allowed_ips: string;
  keep_alive: string;
  name: string;
  configuration: string;
  stats: {
    sent: string,
    received: string,
    handshake: string,
  };

  _expand?: boolean;
  _edit?: boolean;
}
