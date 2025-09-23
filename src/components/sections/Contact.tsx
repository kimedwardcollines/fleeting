import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { MapPin, Phone, Mail, Clock } from 'lucide-react';

const Contact = () => {
  return (
    <section id="contact" className="py-20 bg-soft-gray">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-spiritual mb-4">
            Get In Touch
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            We'd love to hear from you! Whether you have questions, prayer requests, 
            or want to learn more about our church, don't hesitate to reach out.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-12">
          {/* Contact Information */}
          <div className="space-y-8">
            <Card className="p-6">
              <div className="flex items-start space-x-4">
                <MapPin className="w-6 h-6 text-warm-gold mt-1" />
                <div>
                  <h3 className="font-semibold text-spiritual mb-2">Our Location</h3>
                  <p className="text-muted-foreground">
                    Wamala, along Wamala Katoke Road<br />
                    Wamala District, Uganda
                  </p>
                </div>
              </div>
            </Card>

            <Card className="p-6">
              <div className="flex items-start space-x-4">
                <Phone className="w-6 h-6 text-warm-gold mt-1" />
                <div>
                  <h3 className="font-semibold text-spiritual mb-2">Phone</h3>
                  <p className="text-muted-foreground">
                    +256 XXX XXX XXX<br />
                    <span className="text-sm">Call us for prayer requests or information</span>
                  </p>
                </div>
              </div>
            </Card>

            <Card className="p-6">
              <div className="flex items-start space-x-4">
                <Mail className="w-6 h-6 text-warm-gold mt-1" />
                <div>
                  <h3 className="font-semibold text-spiritual mb-2">Email</h3>
                  <p className="text-muted-foreground">
                    info@lavertransformation.org<br />
                    <span className="text-sm">We'll respond within 24 hours</span>
                  </p>
                </div>
              </div>
            </Card>

            <Card className="p-6">
              <div className="flex items-start space-x-4">
                <Clock className="w-6 h-6 text-warm-gold mt-1" />
                <div>
                  <h3 className="font-semibold text-spiritual mb-2">Office Hours</h3>
                  <div className="text-muted-foreground space-y-1">
                    <p>Monday - Friday: 9:00 AM - 5:00 PM</p>
                    <p>Saturday: 10:00 AM - 2:00 PM</p>
                    <p>Sunday: Service Days</p>
                  </div>
                </div>
              </div>
            </Card>
          </div>

          {/* Contact Form */}
          <Card className="p-8">
            <h3 className="text-2xl font-bold text-spiritual mb-6">Send Us A Message</h3>
            <form className="space-y-6">
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-spiritual mb-2">
                    First Name
                  </label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-border rounded-md focus:ring-2 focus:ring-warm-gold focus:border-transparent"
                    placeholder="Your first name"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-spiritual mb-2">
                    Last Name
                  </label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-border rounded-md focus:ring-2 focus:ring-warm-gold focus:border-transparent"
                    placeholder="Your last name"
                  />
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-spiritual mb-2">
                  Email Address
                </label>
                <input
                  type="email"
                  className="w-full px-3 py-2 border border-border rounded-md focus:ring-2 focus:ring-warm-gold focus:border-transparent"
                  placeholder="your.email@example.com"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-spiritual mb-2">
                  Subject
                </label>
                <select className="w-full px-3 py-2 border border-border rounded-md focus:ring-2 focus:ring-warm-gold focus:border-transparent">
                  <option>General Inquiry</option>
                  <option>Prayer Request</option>
                  <option>Youth Ministry</option>
                  <option>Service Information</option>
                  <option>Pastoral Care</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-spiritual mb-2">
                  Message
                </label>
                <textarea
                  rows={5}
                  className="w-full px-3 py-2 border border-border rounded-md focus:ring-2 focus:ring-warm-gold focus:border-transparent"
                  placeholder="How can we help you? Share your prayer requests, questions, or comments..."
                ></textarea>
              </div>
              
              <Button 
                type="submit"
                size="lg"
                className="w-full bg-spiritual hover:bg-spiritual/90 text-white font-semibold transition-all duration-300"
              >
                Send Message
              </Button>
            </form>
          </Card>
        </div>
      </div>
    </section>
  );
};

export default Contact;