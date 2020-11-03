export interface StatusResponse {
  username  : string;
  is_admin : boolean;
  is_infected : boolean;
  being_in_risk_since : string; // FIXME: es una fecha en realidad
  current_location  : boolean;
}