class AccessRight < ActiveRecord::Base
  belongs_to :content
  belongs_to :name
  belongs_to :restriction
  
  
  public name << Name.find(self.name_id) 
  public restriction << Restriction.find(self.restriction_id)
end
